import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from main import app
from db import get_db
from config import settings

# Use a different database for testing
TEST_DATABASE_NAME = f"test_{settings.DATABASE_NAME}"

@pytest_asyncio.fixture(scope="function")
async def client():
    """Fixture to create a test client and override the database dependency."""
    test_client = AsyncIOMotorClient(settings.MONGO_URI)
    test_db = test_client[TEST_DATABASE_NAME]

    # Override the get_db dependency to use the isolated test database
    app.dependency_overrides[get_db] = lambda: test_db

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
    
    # Cleanup: drop the test database and close the client
    await test_client.drop_database(TEST_DATABASE_NAME)
    test_client.close()
    app.dependency_overrides.clear()