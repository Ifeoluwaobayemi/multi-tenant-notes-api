from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class HeaderTenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        x_org = request.headers.get("x-org-id")
        x_user = request.headers.get("x-user-id")
        if x_org and x_user:
            request.state.header_org = x_org
            request.state.header_user = x_user
        return await call_next(request)

async def http_error_handler(request: Request, exc: StarletteHTTPException | RequestValidationError):
    return JSONResponse({"detail": str(exc)}, status_code=getattr(exc, "status_code", 500))
