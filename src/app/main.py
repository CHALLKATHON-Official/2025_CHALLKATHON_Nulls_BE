from fastapi import FastAPI
from app.routes import auth

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
