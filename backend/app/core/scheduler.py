from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.analytics_service import update_all_churn_probabilities
import subprocess
import os

scheduler = BackgroundScheduler()

def retrain_model():
    print("Retraining churn model...")
    result = subprocess.run(
        ["python", "-m", "app.ml.training.churn_training"],
        capture_output=True
    )
    if result.returncode != 0:
        print("Training failed:", result.stderr.decode())
        return
    # Reload model into memory
    from app.ml_inference.churn_predictor import churn_predictor
    churn_predictor.load_model()
    print("Model retrained and reloaded.")

def update_churn_scores():
    print("Updating churn probabilities...")
    db: Session = SessionLocal()
    update_all_churn_probabilities(db)
    db.close()
    print("Churn scores updated.")

def start_scheduler():
    # Retrain every 24 hours
    scheduler.add_job(retrain_model, "interval", hours=24)

    # Update churn probabilities every hour
    scheduler.add_job(update_churn_scores, "interval", hours=1)

    scheduler.start()
    print("Scheduler started.")