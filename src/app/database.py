from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 데이터베이스 URL 설정 (예: SQLite 사용 시)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # 실제 프로젝트에 맞게 변경

# SQLite는 여러 스레드에서 접근할 때 다음 설정이 필요함
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 생성: 데이터베이스와의 연결 관리를 위한 객체
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스: 모든 모델들의 기반 클래스
Base = declarative_base()

def get_db():
    """요청마다 데이터베이스 세션을 생성해 주는 FastAPI 의존성 함수"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()