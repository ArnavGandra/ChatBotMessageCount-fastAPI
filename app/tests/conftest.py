import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base
from app.utils.dependencies import get_db 
from app.main import app

# -----------------------------
# 1. In-memory SQLite for tests
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a sessionmaker bound to the test engine
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -----------------------------
# 2. Create all tables in test DB
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# 3. Override get_db dependency
# -----------------------------
def override_get_db():
    """
    Dependency override for TestClient:
    yields a session connected to the in-memory test DB.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# -----------------------------
# 4. Pytest fixtures
# -----------------------------
@pytest.fixture(scope="function")
def db_session():
    """
    Fixture for direct DB session in tests.
    Use this if you want to manipulate the DB directly.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client():
    """
    Fixture for FastAPI TestClient.
    All requests will use the in-memory DB via dependency override.
    """
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
