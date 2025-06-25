from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from datetime import timedelta
from ..schemas.auth import SignupRequest, LoginRequest, TokenResponse
from ..models.user import User
from ..core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db  # SQLAlchemy 세션 생성 함수

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # 이메일 기준으로 사용자 조회
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="가입된 사용자가 아닙니다."
        )
    
    # 비밀번호 검증
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 올바르지 않습니다."
        )
    
    # JWT 토큰 발급 (data 딕셔너리에 필요한 정보 추가 가능)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires)
    
    return TokenResponse(access_token=access_token)


@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # 이메일 이미 가입되었는지 검사
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 가입된 이메일입니다."
        )
    
    # 추가로 username 중복 여부 검사
    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 아이디입니다."
        )
    
    # 비밀번호를 해시화
    hashed_password = get_password_hash(request.password)
    
    # 새로운 사용자 인스턴스 생성 (User 모델에 맞게 필드들을 삽입)
    new_user = User(
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
        birth_date=request.birth_date
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
