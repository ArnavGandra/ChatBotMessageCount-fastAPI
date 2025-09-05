import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.utils.dependencies import get_db 
from app.models import UserMessageLimit

# Use your actual Postgres database URL
DATABASE_URL = "postgresql://postgres:eAIpassword@database-1.c3y4gguq0fev.us-east-2.rds.amazonaws.com/eai_db"

# Create engine & session for test
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Optional: override get_db for this test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_postgres_connection(db_session):
    """
    Test that we can read/write from the real Postgres table.
    """
    # Clean up any existing test user
    db_session.query(UserMessageLimit).filter(UserMessageLimit.clerk_user_id == "test_integration").delete()
    db_session.commit()

    # Insert a test user
    user = UserMessageLimit(clerk_user_id="test_integration", message_count=1)
    db_session.add(user)
    db_session.commit()

    # Query the user
    fetched_user = db_session.query(UserMessageLimit).filter(UserMessageLimit.clerk_user_id == "test_integration").first()
    assert fetched_user is not None
    assert fetched_user.message_count == 1

    # Update the user
    fetched_user.message_count += 1
    db_session.commit()

    updated_user = db_session.query(UserMessageLimit).filter(UserMessageLimit.clerk_user_id == "test_integration").first()
    assert updated_user.message_count == 2

    # Clean up after test
    db_session.delete(updated_user)
    db_session.commit()
