from fastapi import FastAPI
from routes import auth
from database import Base, engine
from models import user  # 유저 모델을 등록하기 위해 필요함

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app = FastAPI(
    title="My Backend API",
    description="Login and Signup API with FastAPI",
    version="1.0.0"
)

# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the backend API!"}


