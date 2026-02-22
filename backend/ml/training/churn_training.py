import os
import pickle
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LogisticRegression

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # type: ignore

query = """
SELECT 
    u.id as user_id,
    COUNT(e.id) as total_events,
    EXTRACT(DAY FROM NOW() - MAX(e.timestamp)) as days_since_last_event,
    CASE WHEN a.user_id IS NOT NULL THEN 1 ELSE 0 END as experiment_exposed
FROM users u
LEFT JOIN events e ON u.id = e.user_id
LEFT JOIN assignments a ON u.id = a.user_id
GROUP BY u.id, a.user_id
"""

df = pd.read_sql(query, engine)

df["days_since_last_event"] = df["days_since_last_event"].fillna(999)
df["churned"] = (df["days_since_last_event"] > 7).astype(int)

X = df[["total_events", "days_since_last_event", "experiment_exposed"]]
y = df["churned"]

model = LogisticRegression()
model.fit(X, y)

os.makedirs("ml/models", exist_ok=True)

with open("ml/models/churn_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Churn model trained and saved.")