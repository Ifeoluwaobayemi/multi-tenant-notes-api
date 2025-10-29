from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_token

from models.schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/organizations/{org_id}/users/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    try:
        return TokenPayload(**payload)
    except Exception: # Catches Pydantic validation errors
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

def require_roles(allowed: list[str]):
    async def _checker(user: TokenPayload = Depends(get_current_user)):
        if user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return _checker
