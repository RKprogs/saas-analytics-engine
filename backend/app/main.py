from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import auth, links, events, analytics
from app.core.database import Base, engine
from app.core.scheduler import start_scheduler
from app.core.metrics import metrics_middleware, metrics_endpoint
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import time
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    retries = 10
    while retries:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connected and tables created.")
            break
        except Exception:
            print("Database not ready, retrying...")
            time.sleep(3)
            retries -= 1
    if retries == 0:
        raise Exception("Database connection failed after retries.")

    start_scheduler()

    yield

    # Shutdown logic (optional)
    print("Shutting down application.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(metrics_middleware)

app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(links.router, prefix="/api/v1/links")
app.include_router(events.router, prefix="/api/v1/events")
app.include_router(analytics.router, prefix="/api/v1/analytics")
app.add_api_route("/metrics", metrics_endpoint, methods=["GET"])

