import random
import uuid
import os
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.models import (
    User,
    Event,
    Link,
    Click,
    Experiment,
    Variant,
    Assignment
)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)  # type: ignore
Session = sessionmaker(bind=engine)
db = Session()

NOW = datetime.now(timezone.utc)

# ---------------------------
# Helper: realistic churn shaping
# ---------------------------
def generate_user_profile():
    bucket = random.random()

    if bucket < 0.3:  # high churn risk
        total_events = random.randint(1, 5)
        days_since_last = random.randint(10, 20)
    elif bucket < 0.8:  # medium
        total_events = random.randint(6, 20)
        days_since_last = random.randint(3, 9)
    else:  # healthy
        total_events = random.randint(20, 50)
        days_since_last = random.randint(0, 2)

    return total_events, days_since_last


# ---------------------------
# Create Users
# ---------------------------
users = []
for i in range(500):
    created_days_ago = random.randint(0, 30)
    user = User(
        email=f"user{i}@test.com",
        password_hash="fakehash",
        created_at=NOW - timedelta(days=created_days_ago)
    )
    db.add(user)
    users.append(user)

db.commit()

# ---------------------------
# Create Links (20 total)
# ---------------------------
links = []
for i in range(20):
    owner = random.choice(users)
    link = Link(
        original_url="https://example.com/product",
        short_code=str(uuid.uuid4())[:6],
        user_id=owner.id
    )
    db.add(link)
    links.append(link)

db.commit()

# ---------------------------
# Create Experiment + Variants
# ---------------------------
experiment = Experiment(
    name="button_test",
    is_active=True
)
db.add(experiment)
db.commit()

variant_a = Variant(
    experiment_id=experiment.id,
    name="A",
    traffic_percentage=50
)

variant_b = Variant(
    experiment_id=experiment.id,
    name="B",
    traffic_percentage=50
)

db.add_all([variant_a, variant_b])
db.commit()

# ---------------------------
# Assign Users + Create Events
# ---------------------------
for user in users:
    total_events, days_since_last = generate_user_profile()

    # Assign experiment variant (sticky random)
    assigned_variant = random.choice([variant_a, variant_b])
    assignment = Assignment(
        user_id=user.id,
        experiment_id=experiment.id,
        variant_id=assigned_variant.id
    )
    db.add(assignment)

    # Behavioral events
    for _ in range(total_events):
        days_ago = random.randint(0, 30)
        event_type = random.choice(["login", "page_view", "feature_use"])

        event = Event(
            user_id=user.id,
            event_type=event_type,
            event_data={"source": "seed"},
            timestamp=NOW - timedelta(days=days_ago)
        )
        db.add(event)

    # Experiment conversion (Variant B wins intentionally)
    if assigned_variant.name == "A": # type: ignore
        convert_prob = 0.08
    else:
        convert_prob = 0.15

    if random.random() < convert_prob:
        conversion = Event(
            user_id=user.id,
            event_type="experiment_conversion",
            event_data={"experiment": "button_test"},
            timestamp=NOW - timedelta(days=random.randint(0, 10))
        )
        db.add(conversion)

db.commit()

# ---------------------------
# Create Clicks (traffic skew)
# ---------------------------
for link in links:
    if links.index(link) < 3:
        click_volume = random.randint(200, 400)
    else:
        click_volume = random.randint(20, 80)

    for _ in range(click_volume):
        click = Click(
            link_id=link.id,
            ip_address="127.0.0.1",
            user_agent="seed-script",
            timestamp=NOW - timedelta(days=random.randint(0, 30))
        )
        db.add(click)

db.commit()

print("🚀 Seed data created successfully.")