from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.routes import ping
from database import Base, engine
from app.models import user  # 유저 테이블 생성을 위해 필요

# DB 초기화 (모델 기반 테이블 생성)
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="My Backend API",
    description="Login and Signup API with FastAPI",
    version="1.0.0"
)

# ✅ CORS 설정 추가 (프론트엔드 요청 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 프론트엔드 포트에 맞게 조정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(ping.router)                          # 건강 체크용 엔드포인트
app.include_router(auth.router, tags=["Authentication"]) # ✅ prefix 제거

# 기본 루트
@app.get("/")
def read_root():
    return {"message": "Welcome to the backend API!"}