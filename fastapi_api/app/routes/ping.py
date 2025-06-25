from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "✅ 백엔드 연결 성공!"}