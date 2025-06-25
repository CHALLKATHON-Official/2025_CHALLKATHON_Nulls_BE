from sqlalchemy import Column, String, Integer
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # ✅ 수정됨
    birth_date = Column(String, nullable=True)
    nickname = Column(String, unique=True, index=True, nullable=False)