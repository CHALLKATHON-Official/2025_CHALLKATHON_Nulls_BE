from pydantic import BaseModel, EmailStr, validator
from datetime import date
from typing import Optional

class LoginRequest(BaseModel):
    username: str  # ✅ 프론트에서 아이디 입력 받도록 수정됨
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    password_confirm: str
    birth_date: date
    nickname: str   

    @validator("password_confirm")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        return v

class PasswordVerifyRequest(BaseModel):
    password: str

class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    birth_date: Optional[date] = None
    password: Optional[str] = None