from fastapi import APIRouter, Depends, Query, HTTPException, status
from models.schemas import NoteCreate, NoteOut, TokenPayload
from core.auth import get_current_user, require_roles
from services.note_service import NoteService
from db import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteOut, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles(["writer", "admin"]))])
async def create_note(payload: NoteCreate, current: TokenPayload = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    return await NoteService.create(db, current.org_id, current.sub, payload.title, payload.content)

@router.get("/", response_model=list[NoteOut])
async def list_notes(limit: int = Query(20, ge=1, le=100), skip: int = Query(0, ge=0), current: TokenPayload = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    return await NoteService.list(db, current.org_id, skip, limit)

@router.get("/{note_id}", response_model=NoteOut)
async def get_note(note_id: str, current: TokenPayload = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    note = await NoteService.get(db, current.org_id, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_roles(["admin"]))])
async def delete_note(note_id: str, current: TokenPayload = Depends(get_current_user), db: AsyncIOMotorDatabase = Depends(get_db)):
    ok = await NoteService.delete(db, current.org_id, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
