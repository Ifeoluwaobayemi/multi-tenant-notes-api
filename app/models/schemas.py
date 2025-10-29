from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class OrganizationCreate(BaseModel):
    name: str

class OrganizationOut(BaseModel):
    id: str
    name: str
    created_at: datetime

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    email: Optional[EmailStr] = None

class UserOut(BaseModel):
    id: str
    username: str
    role: str
    org_id: str
    email: Optional[EmailStr] = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime

class TokenData(BaseModel):
    access_token: str
    expires_at: datetime

class TokenIn(BaseModel):
    username: str
    password: str

class TokenPayload(BaseModel):
    sub: str # user_id
    org_id: str
    role: str

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteOut(BaseModel):
    id: str
    title: str
    content: str
    org_id: str
    user_id: str
    created_at: datetime
