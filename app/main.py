from fastapi import FastAPI
from routes import organizations, users, notes, auth
from middleware import HeaderTenantMiddleware, http_error_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    app.state.db_client = AsyncIOMotorClient(settings.MONGO_URI)
    yield
    # On shutdown
    app.state.db_client.close()

def create_app():
    app = FastAPI(title="Multi-tenant Notes API", lifespan=lifespan)

    # optional header middleware
    app.add_middleware(HeaderTenantMiddleware)

    # register routes
    app.include_router(organizations.router)
    app.include_router(users.router)
    app.include_router(auth.router)
    app.include_router(notes.router)

    # register basic exception handlers
    app.add_exception_handler(StarletteHTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http_error_handler)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)