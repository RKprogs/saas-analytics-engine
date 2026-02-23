🚀 AI SaaS Intelligence Platform

    A production-grade, zero-cost, full-stack SaaS analytics and intelligence platform built with clean architecture principles, machine learning, experimentation, and infrastructure-as-code.

---

🎯 Overview

    This platform simulates a real SaaS company environment and provides:
        - Link shortener with click analytics
        - User behavioral tracking
        - Retention cohort analysis
        - Churn prediction using machine learning
        - A/B testing statistical engine
        - SQL-based business intelligence console
        - Executive KPI dashboard
        - CI/CD pipeline
        - Dockerized deployment
        - Infrastructure-as-Code (Terraform-ready)

---

🧠 Architecture

Backend:
    - FastAPI
    - PostgreSQL
    - SQLAlchemy
    - Alembic
    - scikit-learn (Logistic Regression)
    - statsmodels (Z-test)

Frontend:
    - Next.js (App Router)
    - TailwindCSS
    - Recharts

DevOps:
    - Docker & Docker Compose
    - GitHub Actions CI
    - Prometheus & Grafana
    - Terraform (local Docker provider)

---

📊 Key Capabilities

🔗 Link Analytics 
- Short link generation
- Click tracking 
- Top link aggregation

📈 Behavioral Analytics 
- DAU / MAU tracking
- Cohort retention 
- Event ingestion (JSONB schema)

🤖 Churn Prediction 
- Feature engineering from behavioral data
- Logistic Regression model
- Model persistence
- Scheduled retraining
- Real-time churn probability API

🧪 Experiment Engine
- Weighted traffic splitting
- Sticky user assignment
- Conversion tracking
- Statistical significance testing (z-test)

📊 SQL Insights Engine
- Secure SELECT-only query execution
- Automatic LIMIT enforcement
- Timeout protection
- Schema access restrictions

🧱 Clean Architecture
- Domain layer separation
- Service layer abstraction
- API layer isolation
- Migration control via Alembic
- Environment-based configuration

---

🐳 Deployment
docker compose up --build

CI runs:
- Dependency install
- DB migration
- Integration tests
- Docker image build

---

📈 Observability
- Prometheus metrics endpoint
- Request latency histograms
- Grafana dashboards

---

🧠 Why This Project Matters

This project demonstrates end-to-end SaaS platform engineering:
- Backend systems design
- ML integration into product workflows
- Experiment-driven optimization
- Secure analytics interfaces
- Infrastructure automation