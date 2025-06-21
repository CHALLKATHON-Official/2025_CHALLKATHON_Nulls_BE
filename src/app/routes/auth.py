from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()

# 요청 데이터 구조 정의
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# 회원가입 엔드포인트
@router.post("/signup")
def signup(request: SignupRequest):
    return {"message": f"User {request.email} signed up successfully."}

# 로그인 엔드포인트
@router.post("/login")
def login(request: LoginRequest):
    if request.email == "test@example.com" and request.password == "password":
        return {"message": "Login successful!"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
