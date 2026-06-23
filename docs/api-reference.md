# API Reference

## Auth

POST /api/v1/auth/signup

POST /api/v1/auth/login

---

## Links

POST /api/v1/links

GET /api/v1/links/{short_code}

---

## Events

POST /api/v1/events

---

## Analytics

GET /api/v1/analytics/dau

GET /api/v1/analytics/mau

GET /api/v1/analytics/rolling-dau

GET /api/v1/analytics/retention/day1

GET /api/v1/analytics/retention/cohort

GET /api/v1/analytics/churn/top-risk

GET /api/v1/analytics/executive

---

## Experiments

POST /api/v1/analytics/experiments/assign/{experiment_name}

GET /api/v1/analytics/experiments/evaluate/{experiment_name}

GET /api/v1/analytics/experiments/churn-impact/{experiment_name}

---

## SQL Insights

POST /api/v1/analytics/sql/query