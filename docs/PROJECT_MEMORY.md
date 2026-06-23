# AI SaaS Intelligence Platform - Project Memory

## Purpose

This project simulates a modern SaaS intelligence platform.

It combines:

- Product analytics
- User event tracking
- Link analytics
- Churn prediction
- A/B testing
- Business intelligence
- Monitoring

The goal is to demonstrate how a SaaS company can collect behavioral data, generate insights, run experiments, and predict customer churn.

---

## Architecture

Frontend:
- Next.js
- TailwindCSS

Backend:
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

ML:
- scikit-learn Logistic Regression

Monitoring:
- Prometheus
- Grafana

DevOps:
- Docker
- Docker Compose
- GitHub Actions

---

## Core Features

### Authentication
JWT-based login and signup.

### Link Shortener
Create short links and track clicks.

### Event Tracking
Capture user behavior:
- login
- page_view
- feature_use
- experiment_conversion

### Analytics
- DAU
- MAU
- Retention
- Top links

### Churn Prediction
Predict probability of user churn using behavioral data.

### Experiment Engine
A/B testing with:
- sticky assignment
- weighted traffic allocation
- z-test significance testing

### SQL Insights
Read-only analytics query interface.

---

## Startup Process

1. Start containers

docker compose up --build

2. Run migrations

alembic upgrade head

3. Seed database

python -m app.scripts.seed_data

4. Train model

python ml/training/churn_training.py

5. Restart backend

docker compose restart backend

---

## Important Endpoints

/api/v1/auth
/api/v1/events
/api/v1/links
/api/v1/analytics

Swagger:

http://localhost:8000/docs