from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth
from app.routes import ping
from app.routes import users        # ✅ 닉네임 중복확인 라우터 추가!

from database import Base, engine
from app.models import user         # ✅ 테이블 생성을 위해 import 필요

# DB 초기화 (모델 기반 테이블 생성)
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="My Backend API",
    description="Login and Signup API with FastAPI",
    version="1.0.0"
)

# ✅ CORS 설정 (프론트 개발용 + 배포용 주소 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",              # 로컬 프론트
        "https://lifec1ock.netlify.app"      # 배포된 프론트
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(ping.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])    # ✅ /users?nickname=... 처리를 위해 추가

# 루트 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Welcome to the backend API!"}