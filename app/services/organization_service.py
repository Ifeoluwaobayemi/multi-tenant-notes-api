from utils import now, oid_to_str
from models.schemas import OrganizationOut
from motor.motor_asyncio import AsyncIOMotorDatabase

class OrganizationService:
    @staticmethod
    async def create(db: AsyncIOMotorDatabase, name: str) -> OrganizationOut:
        doc = {"name": name, "created_at": now()}
        res = await db.organizations.insert_one(doc)
        return OrganizationOut(id=oid_to_str(res.inserted_id), name=name, created_at=doc["created_at"])
