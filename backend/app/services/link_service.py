import random
import string
from sqlalchemy.orm import Session
from app.infrastructure.database.models import Link

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_short_link(db: Session, original_url: str, user_id):
    short_code = generate_short_code()
    link = Link(
        original_url=original_url,
        short_code=short_code,
        user_id=user_id
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link