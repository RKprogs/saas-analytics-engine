import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database.models import User, Event, Link, Click
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # type: ignore
Session = sessionmaker(bind=engine)
db = Session()

# Create Users
users = []
for i in range(50):
    user = User(
        email=f"user{i}@test.com",
        password_hash="fakehash",
        created_at=datetime.utcnow() - timedelta(days=random.randint(0, 10))
    )
    db.add(user)
    users.append(user)

db.commit()

# Create Links
links = []
for user in users:
    link = Link(
        original_url="https://example.com",
        short_code=str(uuid.uuid4())[:6],
        user_id=user.id
    )
    db.add(link)
    links.append(link)

db.commit()

# Create Events
for user in users:
    for _ in range(random.randint(1, 5)):
        event = Event(
            user_id=user.id,
            event_type="page_view",
            event_data={"page": "dashboard"},
            timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 10))
        )
        db.add(event)

db.commit()

# Create Clicks
for link in links:
    for _ in range(random.randint(1, 10)):
        click = Click(
            link_id=link.id,
            ip_address="127.0.0.1",
            user_agent="seed-script",
            timestamp=datetime.utcnow() - timedelta(days=random.randint(0, 10))
        )
        db.add(click)

db.commit()

print("Seed data created.")