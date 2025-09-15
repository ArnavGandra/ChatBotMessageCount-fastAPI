"""
Business logic layer (Service).
Applies rules: 20 message limit, 12-hour cooldown.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from . import crud
from .exceptions import LimitExceededException

MESSAGE_LIMIT = 20
COOLDOWN_HOURS = 12

def process_message(db: Session, user_id: str):
    """
    Handles message attempt:
    - Creates user record if not exists
    - Resets counter if cooldown expired
    - Raises exception if limit reached
    - Increments counter if allowed
    """
    now = datetime.now(timezone.utc)
    user = crud.get_user_limit(db, user_id)

    if not user:
        user = crud.create_user_limit(db, user_id)

    # Reset counter if cooldown has expired
    elapsed =  now - user.last_reset
    if elapsed > timedelta(hours=COOLDOWN_HOURS):
        user.message_count = 0
        user.last_reset = now
        crud.save_user(db, user)

    # Check limit
    if user.message_count >= MESSAGE_LIMIT:
        raise LimitExceededException(wait_hours=COOLDOWN_HOURS)

    # Increment usage
    user.message_count += 1
    crud.save_user(db, user)

    return user
