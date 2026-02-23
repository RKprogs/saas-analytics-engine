from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.experiment_service import assign_user_to_experiment, churn_by_variant, evaluate_experiment
from app.core.dependencies import get_current_user
from app.infrastructure.database.models import User
from app.services.analytics_service import get_daily_active_users, get_rolling_dau, get_mau, get_top_churn_risk_users, update_all_churn_probabilities
from app.services.analytics_service import get_day1_retention, get_cohort_retention
from app.services.analytics_service import generate_churn_features, get_user_churn_features, get_executive_metrics
from app.ml_inference.churn_predictor import churn_predictor
from app.services.analytics_service import (
    get_click_count_for_link,
    get_top_links,
    get_clicks_by_day
)


router = APIRouter()

@router.get("/dau")
def daily_active_users(db: Session = Depends(get_db)):
    dau = get_daily_active_users(db)
    return {"daily_active_users": dau}

@router.get("/links/{link_id}/clicks")
def click_count(link_id: str, db: Session = Depends(get_db)):
    return {
        "clicks": get_click_count_for_link(db, link_id)
    }

@router.get("/top-links")
def top_links(db: Session = Depends(get_db)):
    results = get_top_links(db)
    return [
        {"short_code": r[0], "clicks": r[1]}
        for r in results
    ]

@router.get("/clicks-by-day")
def clicks_by_day(db: Session = Depends(get_db)):
    results = get_clicks_by_day(db)
    return [
        {"date": str(r[0]), "clicks": r[1]}
        for r in results
    ]

@router.get("/retention/day1")
def day1_retention(db: Session = Depends(get_db)):
    return {
        "day1_retention_percent": get_day1_retention(db)
    }

@router.get("/rolling-dau")
def rolling_dau(days: int = 7, db: Session = Depends(get_db)):
    return {
        "rolling_active_users": get_rolling_dau(db, days)
    }

@router.get("/mau")
def mau(db: Session = Depends(get_db)):
    return {"monthly_active_users": get_mau(db)}

@router.get("/retention/cohort")
def cohort_retention(max_days: int = 7, db: Session = Depends(get_db)):
    return get_cohort_retention(db, max_days)

@router.get("/churn/features")
def churn_features(db: Session = Depends(get_db)):
    return generate_churn_features(db)

@router.get("/churn/predict/{user_id}")
def predict_churn(user_id: str, db: Session = Depends(get_db)):
    total_events, days_since_last_event = get_user_churn_features(db, user_id)

    probability = churn_predictor.predict(
        total_events,
        days_since_last_event
    )

    if probability is None:
        return {"error": "Model not loaded"}

    return {
        "user_id": user_id,
        "churn_probability": probability
    }

@router.post("/churn/update-all")
def update_churn(db: Session = Depends(get_db)):
    return update_all_churn_probabilities(db)

@router.get("/executive")
def executive_dashboard(db: Session = Depends(get_db)):
    return get_executive_metrics(db)

@router.post("/experiments/assign/{experiment_name}")
def assign_experiment(
    experiment_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    variant_id = assign_user_to_experiment(
        db,
        current_user.id,
        experiment_name
    )

    if variant_id is None:
        return {"error": "Experiment not found"}

    return {"variant_id": str(variant_id)}

@router.get("/experiments/evaluate/{experiment_name}")
def evaluate_experiment_endpoint(
    experiment_name: str,
    db: Session = Depends(get_db)
):
    return evaluate_experiment(db, experiment_name)

@router.get("/experiments/churn-impact/{experiment_name}")
def churn_impact(experiment_name: str, db: Session = Depends(get_db)):
    return churn_by_variant(db, experiment_name)

@router.get("/churn/top-risk")
def top_risk_users(limit: int = 10, db: Session = Depends(get_db)):
    return get_top_churn_risk_users(db, limit)