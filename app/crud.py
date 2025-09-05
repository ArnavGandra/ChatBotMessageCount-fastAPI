"""
CRUD operations for database access.
Keep raw SQLAlchemy logic separate from business logic.
"""

from sqlalchemy.orm import Session
from . import models

def get_user_limit(db: Session, user_id: str):
    return db.query(models.UserMessageLimit).filter(models.UserMessageLimit.clerk_user_id == user_id).first()

def create_user_limit(db: Session, user_id: str):
    user = models.UserMessageLimit(clerk_user_id=user_id, message_count=0)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_user(db: Session, user: models.UserMessageLimit):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
