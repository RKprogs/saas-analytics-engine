from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.event_service import log_event
from app.core.dependencies import get_current_user
from app.infrastructure.database.models import User

router = APIRouter()

@router.post("/")
def create_event(
    event_type: str,
    metadata: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = log_event(db, current_user.id, event_type, metadata)
    return {"id": str(event.id), "event_type": event.event_type}