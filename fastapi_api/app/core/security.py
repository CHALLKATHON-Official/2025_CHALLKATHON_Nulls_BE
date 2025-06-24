from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

# 비밀번호 해싱/검증을 위한 컨텍스트 (bcrypt 권장)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 관련 설정
SECRET_KEY = "your-secret-key"  # 실제 서비스에서는 안전하게 관리할 것
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

