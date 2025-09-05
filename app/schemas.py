"""
Pydantic schemas for request/response validation.
"""

from pydantic import BaseModel
from datetime import datetime

class UserMessageLimitResponse(BaseModel):
    clerk_user_id: str
    message_count: int
    last_reset: datetime

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    success: bool
    message: str
    usage: str | None = None
