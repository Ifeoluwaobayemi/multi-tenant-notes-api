from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from fastapi import Request

def get_client():
    raise NotImplementedError("get_client should not be called directly. Use dependency injection.")

def get_db(request: Request):
    return request.app.state.db_client[settings.DATABASE_NAME]
