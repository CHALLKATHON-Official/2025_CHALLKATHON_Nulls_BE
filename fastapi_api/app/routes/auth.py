from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

from ..schemas.auth import SignupRequest, LoginRequest, TokenResponse
from ..models.user import User
from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from database import get_db

from app.auth_utils import get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()  # ✅ 수정됨
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="가입된 사용자가 아닙니다.",
        )

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 올바르지 않습니다.",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )

    return TokenResponse(access_token=access_token)

@router.post("/users")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    try:
        print("📨 회원가입 요청:", request.dict())

        existing_email = db.query(User).filter(User.email == request.email).first()
        if existing_email:
            print("⚠️ 중복된 이메일")
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

        existing_username = db.query(User).filter(User.username == request.username).first()
        if existing_username:
            print("⚠️ 중복된 아이디")
            raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")

        hashed_password = get_password_hash(request.password)

        new_user = User(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            birth_date=request.birth_date
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("✅ 회원가입 성공:", new_user.username)
        return {"message": "회원가입 완료"}

    except IntegrityError as ie:
        db.rollback()
        print("❌ DB 제약조건 오류:", str(ie))
        raise HTTPException(status_code=400, detail="중복된 필드로 인해 저장에 실패했습니다.")
    except Exception as e:
        db.rollback()
        print("🔥 예외 발생:", str(e))
        raise HTTPException(status_code=500, detail="서버 내부 오류입니다.")
    
@router.get("/me")
def get_my_info(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "birth_date": current_user.birth_date,
    }