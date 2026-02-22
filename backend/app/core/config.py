import os

class Settings:
    PROJECT_NAME = "AI SaaS Intelligence Platform"
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

settings = Settings()