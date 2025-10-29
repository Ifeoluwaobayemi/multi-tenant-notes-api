from fastapi import APIRouter, status, Depends
from models.schemas import OrganizationCreate, OrganizationOut
from services.organization_service import OrganizationService
from db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("/", response_model=OrganizationOut, status_code=status.HTTP_201_CREATED)
async def create_org(payload: OrganizationCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    return await OrganizationService.create(db, payload.name)
