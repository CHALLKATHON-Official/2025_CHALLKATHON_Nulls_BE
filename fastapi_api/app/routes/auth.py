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
    get_current_user,  # ✅ 로그인된 유저 정보를 가져오는 함수
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
        print("📨 회원가입 요청:", request.dict())

        existing_email = db.query(User).filter(User.email == request.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

        existing_username = db.query(User).filter(User.username == request.username).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")

        existing_nickname = db.query(User).filter(User.nickname == request.nickname).first()
        if existing_nickname:
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
        print("✅ 회원가입 성공:", new_user.username)
        return {"message": "회원가입 완료"}

    except IntegrityError as ie:
        db.rollback()
        raise HTTPException(status_code=400, detail="중복된 필드로 인해 저장에 실패했습니다.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="서버 내부 오류입니다.")


@router.get("/users/check-nickname")
def check_nickname(nickname: str, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.nickname == nickname).first() is not None
    return {"exists": exists}


# ✅ 로그인된 사용자 정보 가져오기
@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "email": current_user.email,
        "birth_date": current_user.birth_date,
    }