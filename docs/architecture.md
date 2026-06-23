# Architecture

## High-Level Architecture

Frontend (Next.js)
        |
        v
FastAPI API Layer
        |
        v
Service Layer
        |
        v
SQLAlchemy ORM
        |
        v
PostgreSQL

Analytics Services
Experiment Engine
Churn Prediction Engine

Prometheus
     |
Grafana

---

## Layer Responsibilities

### API Layer

Handles:
- HTTP requests
- validation
- authentication

Files:

app/api/v1/

---

### Service Layer

Contains business logic.

Files:

app/services/

Examples:

- analytics_service.py
- experiment_service.py
- user_service.py

---

### Data Layer

SQLAlchemy models.

Files:

app/infrastructure/database/models.py

---

### ML Layer

Training:

ml/training/churn_training.py

Inference:

app/ml_inference/churn_predictor.py

---

### Monitoring Layer

Prometheus scrapes metrics.

Grafana visualizes metrics.