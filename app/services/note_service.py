from fastapi import HTTPException
from bson import ObjectId
from utils import oid_to_str, now
from models.schemas import NoteOut
from motor.motor_asyncio import AsyncIOMotorDatabase

class NoteService:
    @staticmethod
    async def create(db: AsyncIOMotorDatabase, org_id: str, user_id: str, title: str, content: str) -> NoteOut:
        doc = {"org_id": ObjectId(org_id), "user_id": ObjectId(user_id), "title": title, "content": content, "created_at": now()}
        res = await db.notes.insert_one(doc)
        return NoteOut(id=oid_to_str(res.inserted_id), title=title, content=content, org_id=org_id, user_id=user_id, created_at=doc["created_at"])

    @staticmethod
    async def list(db: AsyncIOMotorDatabase, org_id: str, skip: int = 0, limit: int = 20) -> list[NoteOut]:
        cursor = db.notes.find({"org_id": ObjectId(org_id)}).sort("created_at", -1).skip(skip).limit(limit)
        out = []
        async for n in cursor:
            out.append(NoteOut(id=oid_to_str(n["_id"]), title=n["title"], content=n["content"], org_id=oid_to_str(n["org_id"]), user_id=oid_to_str(n["user_id"]), created_at=n["created_at"]))
        return out

    @staticmethod
    async def get(db: AsyncIOMotorDatabase, org_id: str, note_id: str) -> NoteOut | None:
        n = await db.notes.find_one({"_id": ObjectId(note_id), "org_id": ObjectId(org_id)})
        if not n:
            return None
        return NoteOut(id=oid_to_str(n["_id"]), title=n["title"], content=n["content"], org_id=oid_to_str(n["org_id"]), user_id=oid_to_str(n["user_id"]), created_at=n["created_at"])

    @staticmethod
    async def delete(db: AsyncIOMotorDatabase, org_id: str, note_id: str):
        res = await db.notes.delete_one({"_id": ObjectId(note_id), "org_id": ObjectId(org_id)})
        return res.deleted_count > 0
