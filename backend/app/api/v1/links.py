from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.core.database import get_db
from app.services.link_service import create_short_link
from app.infrastructure.database.models import Link, User
from app.services.click_service import log_click
from app.core.dependencies import get_current_user
from app.schemas.link import LinkCreate

router = APIRouter()

@router.post("/")
def create_link(
    link_data: LinkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    link = create_short_link(db, link_data.original_url, current_user.id)
    return {"short_code": link.short_code}

@router.get("/{short_code}")
def redirect(short_code: str, request: Request, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.short_code == short_code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    log_click(
        db,
        link.id,
        request.client.host if request.client else None,
        request.headers.get("user-agent")
    )

    return RedirectResponse(str(link.original_url))