from sqlalchemy.orm import Session
from app.infrastructure.database.models import Event

def log_event(db: Session, user_id, event_type: str, metadata: dict):
    event = Event(
        user_id=user_id,
        event_type=event_type,
        event_data=metadata
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event