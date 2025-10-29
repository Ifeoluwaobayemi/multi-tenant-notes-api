from fastapi import APIRouter, Depends
from models.schemas import TokenOut, TokenIn
from services.user_service import UserService
from db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/organizations/{org_id}/users", tags=["authentication"])

@router.post("/login", response_model=TokenOut)
async def login(org_id: str, payload: TokenIn, db: AsyncIOMotorDatabase = Depends(get_db)):
    data = await UserService.login(db, org_id, payload.username, payload.password)
    return TokenOut(access_token=data.access_token, expires_at=data.expires_at)