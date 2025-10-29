from fastapi import HTTPException, status
from bson import ObjectId
from models.schemas import TokenData, UserOut
from core.security import hash_password, verify_password, create_access_token
from utils import oid_to_str, now
from motor.motor_asyncio import AsyncIOMotorDatabase

class UserService:
    @staticmethod
    async def create(db: AsyncIOMotorDatabase, org_id: str, username: str, password: str, role: str, email: str | None) -> UserOut:
        org = await db.organizations.find_one({"_id": ObjectId(org_id)})
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        exists = await db.users.find_one({"org_id": ObjectId(org_id), "username": username})
        if exists:
            raise HTTPException(status_code=400, detail="Username already exists in organization")
        hashed = hash_password(password)
        doc = {"org_id": ObjectId(org_id), "username": username, "hashed_password": hashed, "role": role, "email": email, "created_at": now()}
        res = await db.users.insert_one(doc)
        return UserOut(id=oid_to_str(res.inserted_id), username=username, role=role, org_id=org_id, email=email)

    @staticmethod
    async def login(db: AsyncIOMotorDatabase, org_id: str, username: str, password: str) -> TokenData:
        user = await db.users.find_one({"org_id": ObjectId(org_id), "username": username})
        if not user or not verify_password(password, user["hashed_password"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token_data = {"sub": oid_to_str(user["_id"]), "org_id": oid_to_str(user["org_id"]), "role": user["role"]}
        token, exp = create_access_token(token_data)
        return TokenData(access_token=token, expires_at=exp)
