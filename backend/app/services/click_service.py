from sqlalchemy.orm import Session
from app.infrastructure.database.models import Click

def log_click(db: Session, link_id, ip, user_agent):
    click = Click(
        link_id=link_id,
        ip_address=ip,
        user_agent=user_agent
    )
    db.add(click)
    db.commit()
    db.refresh(click)
    return click