# tests/test_db.py

import pytest
from sqlalchemy import inspect
from app.database import engine
from app.models import UserMessageLimit

def test_tables_exist():
    """
    Test that the database connection works and the user_message_limits table exists.
    """
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    # Check if our table exists
    assert "user_message_limits" in tables, "user_message_limits table does not exist in the DB"

def test_can_insert_user():
    """
    Test that we can insert a row into user_message_limits table.
    """
    from sqlalchemy.orm import Session

    with Session(engine) as session:
        # Clean up any existing test user
        session.query(UserMessageLimit).filter_by(clerk_user_id="test_user").delete()
        session.commit()

        # Insert test user
        user = UserMessageLimit(clerk_user_id="test_user")
        session.add(user)
        session.commit()

        # Retrieve the user
        retrieved = session.get(UserMessageLimit, "test_user")
        assert retrieved is not None
        assert retrieved.message_count == 0

