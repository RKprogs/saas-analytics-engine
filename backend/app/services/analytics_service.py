from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import date, timedelta, datetime, timezone
from app.infrastructure.database.models import Event, Click, Link, User, Assignment

def get_daily_active_users(db: Session):
    today = date.today()

    dau = (
        db.query(func.count(func.distinct(Event.user_id)))
        .filter(func.date(Event.timestamp) == today)
        .scalar()
    )

    return dau or 0

def get_click_count_for_link(db: Session, link_id):
    return (
        db.query(func.count(Click.id))
        .filter(Click.link_id == link_id)
        .scalar()
    ) or 0

def get_top_links(db: Session, limit: int = 5):
    return (
        db.query(
            Link.short_code,
            func.count(Click.id).label("click_count")
        )
        .join(Click, Click.link_id == Link.id)
        .group_by(Link.short_code)
        .order_by(func.count(Click.id).desc())
        .limit(limit)
        .all()
    )

def get_clicks_by_day(db: Session):
    return (
        db.query(
            cast(Click.timestamp, Date).label("date"),
            func.count(Click.id).label("clicks")
        )
        .group_by(cast(Click.timestamp, Date))
        .order_by(cast(Click.timestamp, Date))
        .all()
    )

def get_day1_retention(db: Session):
    # Users who signed up yesterday
    yesterday = func.current_date() - timedelta(days=1)

    cohort_select = (
        db.query(User.id)
        .filter(func.date(User.created_at) == yesterday)
    )

    # Users from that cohort who were active today
    retained_users = (
        db.query(func.count(func.distinct(Event.user_id)))
        .filter(
            Event.user_id.in_(cohort_select),
            func.date(Event.timestamp) == func.current_date()
        )
        .scalar()
    )

    cohort_users = cohort_select.subquery()
    total_cohort = db.query(func.count()).select_from(cohort_users).scalar()

    if total_cohort == 0:
        return 0

    return round((retained_users / total_cohort) * 100, 2)

def get_rolling_dau(db: Session, days: int = 7):
    cutoff = datetime.utcnow() - timedelta(days=days)

    count = (
        db.query(func.count(func.distinct(Event.user_id)))
        .filter(Event.timestamp >= cutoff)
        .scalar()
    )

    return count or 0

def get_mau(db: Session):
    cutoff = datetime.utcnow() - timedelta(days=30)

    return (
        db.query(func.count(func.distinct(Event.user_id)))
        .filter(Event.timestamp >= cutoff)
        .scalar()
    ) or 0

def get_cohort_retention(db: Session, max_days: int = 7):
    # Step 1: Fetch users grouped by signup date
    users = db.query(User.id, func.date(User.created_at)).all()

    cohorts = defaultdict(list)
    for user_id, signup_date in users:
        cohorts[signup_date].append(user_id)

    results = {}

    for cohort_date, user_ids in cohorts.items():
        cohort_size = len(user_ids)
        results[str(cohort_date)] = {}

        for day in range(max_days + 1):
            target_date = cohort_date + timedelta(days=day)

            active_count = (
                db.query(func.count(func.distinct(Event.user_id)))
                .filter(
                    Event.user_id.in_(user_ids),
                    func.date(Event.timestamp) == target_date
                )
                .scalar()
            )

            if cohort_size == 0:
                retention = 0
            else:
                retention = round((active_count / cohort_size) * 100, 2)

            results[str(cohort_date)][f"day_{day}"] = retention

    return results

def get_user_experiment_flag(db: Session, user_id):
    assignment = (
        db.query(Assignment)
        .filter(Assignment.user_id == user_id)
        .first()
    )

    if assignment:
        return 1
    return 0

def generate_churn_features(db: Session, inactivity_days: int = 7):
    cutoff = datetime.now(timezone.utc) - timedelta(days=inactivity_days)

    users = db.query(User).all()
    features = []

    for user in users:
        total_events = (
            db.query(func.count(Event.id))
            .filter(Event.user_id == user.id)
            .scalar()
        )

        last_event = (
            db.query(func.max(Event.timestamp))
            .filter(Event.user_id == user.id)
            .scalar()
        )

        days_since_last_event = None
        if last_event:
            now = datetime.now(timezone.utc)
            days_since_last_event = (now - last_event).days
        else:
            days_since_last_event = 999  # never active

        churned = last_event is None or last_event < cutoff

        experiment_flag = get_user_experiment_flag(db, user.id)

        features.append({
            "user_id": str(user.id),
            "total_events": total_events,
            "days_since_last_event": days_since_last_event,
            "experiment_exposed": experiment_flag,
            "churned": int(churned)
        })

    return features

def get_user_churn_features(db: Session, user_id):
    total_events = (
        db.query(func.count(Event.id))
        .filter(Event.user_id == user_id)
        .scalar()
    )

    last_event = (
        db.query(func.max(Event.timestamp))
        .filter(Event.user_id == user_id)
        .scalar()
    )

    if last_event:
        now = datetime.now(timezone.utc)
        days_since_last_event = (now - last_event).days
    else:
        days_since_last_event = 999

    return total_events, days_since_last_event

def update_all_churn_probabilities(db: Session):
    users = db.query(User).all()

    from app.ml_inference.churn_predictor import churn_predictor

    for user in users:
        total_events, days_since_last_event = get_user_churn_features(db, user.id)

        probability = churn_predictor.predict(
            total_events,
            days_since_last_event
        )

        user.churn_probability = probability # type: ignore

    db.commit()

    return {"updated_users": len(users)}

def get_executive_metrics(db: Session):
    total_users = db.query(func.count(User.id)).scalar()
    dau = get_daily_active_users(db)
    mau = get_mau(db)

    avg_churn = db.query(func.avg(User.churn_probability)).scalar() or 0

    high_risk = db.query(func.count(User.id))\
        .filter(User.churn_probability > 0.7)\
        .scalar()

    return {
        "total_users": total_users,
        "daily_active_users": dau,
        "monthly_active_users": mau,
        "average_churn_probability": round(float(avg_churn), 4),
        "high_risk_users": high_risk
    }

