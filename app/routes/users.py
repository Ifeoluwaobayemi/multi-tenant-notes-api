from fastapi import APIRouter, status, Depends
from models.schemas import UserCreate, UserOut
from services.user_service import UserService
from db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/organizations/{org_id}/users", tags=["users"])

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(org_id: str, payload: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await UserService.create(db, org_id, payload.username, payload.password, payload.role, payload.email)
