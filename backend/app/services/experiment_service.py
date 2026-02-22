import random
import math
import warnings
from sqlalchemy.orm import Session
from app.infrastructure.database.models import Experiment, User, Variant, Assignment, Event
from statsmodels.stats.proportion import proportions_ztest
from sqlalchemy import func, select

def assign_user_to_experiment(db: Session, user_id, experiment_name):
    # 1️⃣ Get active experiment
    experiment = (
        db.query(Experiment)
        .filter(
            Experiment.name == experiment_name,
            Experiment.is_active.is_(True)
        )
        .first()
    )

    if not experiment:
        return None

    # 2️⃣ Check existing assignment (sticky behavior)
    existing = (
        db.query(Assignment)
        .filter(
            Assignment.user_id == user_id,
            Assignment.experiment_id == experiment.id
        )
        .first()
    )

    if existing:
        return existing.variant_id

    # 3️⃣ Load variants
    variants = (
        db.query(Variant)
        .filter(Variant.experiment_id == experiment.id)
        .all()
    )

    if not variants:
        return None

    # 4️⃣ Weighted random assignment
    rand = random.randint(1, 100)
    cumulative = 0
    selected_variant = None

    for variant in variants:
        # Access raw value safely
        traffic = variant.__dict__["traffic_percentage"]
        cumulative += traffic

        if rand <= cumulative:
            selected_variant = variant
            break

    # 5️⃣ Fallback safety (if percentages don't sum to 100)
    if selected_variant is None:
        selected_variant = variants[-1]

    # 6️⃣ Create assignment
    assignment = Assignment(
        user_id=user_id,
        experiment_id=experiment.id,
        variant_id=selected_variant.id
    )

    db.add(assignment)
    db.commit()

    return selected_variant.id

def evaluate_experiment(db: Session, experiment_name: str):

    # 1️⃣ Fetch experiment safely
    experiment = (
        db.query(Experiment)
        .filter(Experiment.name == experiment_name)
        .first()
    )

    if experiment is None:
        return {"error": "Experiment not found"}

    # 2️⃣ Fetch variants
    variants = (
        db.query(Variant)
        .filter(Variant.experiment_id == experiment.id)
        .all()
    )

    if len(variants) < 2:
        return {"error": "At least 2 variants required"}

    results = []

    for variant in variants:

        # Total assigned users
        total_users = (
            db.query(func.count(Assignment.id))
            .filter(Assignment.variant_id == variant.id)
            .scalar()
        )

        # Users assigned to this variant
        assigned_user_ids = select(Assignment.user_id).where(
            Assignment.variant_id == variant.id
        )

        # Conversion events for this variant
        conversions = (
            db.query(func.count(func.distinct(Event.user_id)))
            .filter(
                Event.user_id.in_(assigned_user_ids),
                Event.event_type == "experiment_conversion",
                Event.event_data["experiment"].astext == experiment_name
            )
            .scalar()
        )

        conversion_rate = 0
        if total_users and total_users > 0:
            conversion_rate = conversions / total_users

        results.append({
            "variant_name": variant.name,
            "total_users": total_users,
            "conversions": conversions,
            "conversion_rate": round(conversion_rate, 4)
        })

    # 3️⃣ Only handle 2-variant experiments for now
    if len(results) == 2:
        count = [results[0]["conversions"], results[1]["conversions"]]
        nobs = [results[0]["total_users"], results[1]["total_users"]]

        # Prevent division-by-zero crash
        if min(nobs) == 0:
            return {
                "variants": results,
                "message": "Not enough data for statistical test"
            }

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            stat, pval = proportions_ztest(count, nobs)

        if pval is None or math.isnan(pval) or math.isinf(pval):
            return {
                "variants": results,
                "message": "Statistical test inconclusive (insufficient variance)"
            }

        return {
            "variants": results,
            "p_value": round(float(pval), 5)
        }

    return {
        "variants": results,
        "message": "Statistical test only implemented for 2 variants"
    }

def churn_by_variant(db: Session, experiment_name: str):
    experiment = (
        db.query(Experiment)
        .filter(Experiment.name == experiment_name)
        .first()
    )

    if not experiment:
        return {"error": "Experiment not found"}

    variants = db.query(Variant)\
        .filter(Variant.experiment_id == experiment.id)\
        .all()

    results = []

    for variant in variants:
        user_ids = select(Assignment.user_id).where(
            Assignment.variant_id == variant.id
        )

        avg_churn = (
            db.query(func.avg(User.churn_probability))
            .filter(User.id.in_(user_ids))
            .scalar()
        )

        results.append({
            "variant_name": variant.name,
            "average_churn_probability": round(float(avg_churn or 0), 4)
        })

    return results