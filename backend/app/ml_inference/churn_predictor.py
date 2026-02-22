import pickle
import os
import numpy as np
import pandas as pd

BASE_DIR = os.getcwd()
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "churn_model.pkl")

class ChurnPredictor:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        print("Looking for model at:", MODEL_PATH)

        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            print("Churn model loaded.")
        else:
            print("Churn model not found.")

    def predict(self, total_events, days_since_last_event, experiment_exposed = 0):
        if not self.model:
            return None

        X = pd.DataFrame([{
            "total_events": total_events,
            "days_since_last_event": days_since_last_event,
            "experiment_exposed": experiment_exposed
        }])

        X = X.reindex(columns=self.model.feature_names_in_, fill_value=0)
        probability = self.model.predict_proba(X)[0][1]
        return round(float(probability), 4)


# Singleton instance
churn_predictor = ChurnPredictor()