import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import message_history
import uuid

client = TestClient(app)

# ---------------------------
# Fixtures
# ---------------------------
@pytest.fixture(scope="module")
def db():
    # Create tables for tests
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def create_user(db):
    username = f"testuser_{uuid.uuid4().hex[:6]}"
    user = message_history.User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---------------------------
# Tests
# ---------------------------

def test_save_user_message(db, create_user):
    user_id = create_user.id
    payload = {
        "user_id": user_id,
        "role": "user",
        "content": "Hello AI!"
    }
    response = client.post("/messages/save-message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["role"] == "user"
    assert data["content"] == "Hello AI!"
    assert "id" in data
    assert "timestamp" in data

def test_save_assistant_message(db, create_user):
    user_id = create_user.id
    payload = {
        "user_id": user_id,
        "role": "assistant",
        "content": "Hi! How can I help?"
    }
    response = client.post("/messages/save-message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["role"] == "assistant"
    assert data["content"] == "Hi! How can I help?"

def test_get_message_history(db, create_user):
    user_id = create_user.id

    # Save messages first
    client.post("/messages/save-message", json={
        "user_id": user_id,
        "role": "user",
        "content": "Message 1"
    })
    client.post("/messages/save-message", json={
        "user_id": user_id,
        "role": "assistant",
        "content": "Reply 1"
    })

    # Get history
    response = client.get(f"/messages/history/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    roles = [msg["role"] for msg in data]
    contents = [msg["content"] for msg in data]
    assert "user" in roles
    assert "assistant" in roles
    assert "Message 1" in contents
    assert "Reply 1" in contents

