from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", tags=["root"])
async def pong():
    return {"ping": "pong!"}
