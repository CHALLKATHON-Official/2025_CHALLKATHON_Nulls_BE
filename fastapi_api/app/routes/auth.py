from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
import os

from ..schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    PasswordVerifyRequest,
    UserUpdateRequest,
)
from ..models.user import User
from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user,
)
from database import get_db

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
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
        if db.query(User).filter(User.email == request.email).first():
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")
        if db.query(User).filter(User.username == request.username).first():
            raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")
        if db.query(User).filter(User.nickname == request.nickname).first():
            raise HTTPException(status_code=400, detail="이미 사용 중인 별명입니다.")

        hashed_password = get_password_hash(request.password)
        new_user = User(
            username=request.username,
            email=request.email,
            hashed_password=hashed_password,
            birth_date=request.birth_date,
            nickname=request.nickname,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "회원가입 완료"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="중복된 필드로 인해 저장에 실패했습니다.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="서버 내부 오류입니다.")

@router.get("/users/check-nickname")
def check_nickname(nickname: str, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.nickname == nickname).first() is not None
    return {"exists": exists}

@router.get("/me")
def get_my_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "email": current_user.email,
        "birth_date": current_user.birth_date,
    }

@router.post("/verify-password")
def verify_password_route(
    request: PasswordVerifyRequest,
    current_user: User = Depends(get_current_user)
):
    if not verify_password(request.password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail="비밀번호가 올바르지 않습니다.")
    return {"message": "비밀번호 확인 완료"}

@router.patch("/users/me")
def update_my_info(
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.nickname:
        current_user.nickname = payload.nickname
    if payload.email:
        current_user.email = payload.email
    if payload.birth_date:
        current_user.birth_date = payload.birth_date
    if payload.password:
        current_user.hashed_password = get_password_hash(payload.password)

    try:
        db.commit()
        db.refresh(current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="정보 수정 중 오류가 발생했습니다.")

    return {"message": "정보 수정 완료"}
