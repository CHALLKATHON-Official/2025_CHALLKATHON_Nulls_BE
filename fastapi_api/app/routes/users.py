from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/check-nickname")
def check_nickname(nickname: str = Query(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.nickname == nickname).first()
    if existing_user:
        return {"available": False}
    return {"available": True}