from bson import ObjectId
from datetime import datetime

def oid_to_str(oid: ObjectId | str) -> str:
    return str(oid)

def now() -> datetime:
    return datetime.utcnow()
