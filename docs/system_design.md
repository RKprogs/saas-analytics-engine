# System Design

## User Signup Flow

User
  |
POST /signup
  |
FastAPI
  |
User Service
  |
PostgreSQL

---

## Event Tracking Flow

User Action
    |
POST /events
    |
Event Service
    |
events table

---

## Churn Prediction Flow

events table
      |
Feature Generation
      |
Logistic Regression
      |
churn_probability

---

## Experiment Flow

User
  |
Experiment Assignment
  |
Variant A/B
  |
Conversion Event
  |
Statistical Evaluation

---

## Analytics Flow

Events
  |
Aggregation
  |
Analytics Service
  |
Dashboard