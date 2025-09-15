"""
SQLAlchemy ORM models.
"""

from sqlalchemy import Column, String, Integer, TIMESTAMP, func
from .database import Base

class UserMessageLimit(Base):
    __tablename__ = "user_message_limits"

    clerk_user_id = Column(String, primary_key=True, index=True)
    message_count = Column(Integer, default=0)
    last_reset = Column(TIMESTAMP(timezone=True), server_default=func.now())
