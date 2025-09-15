from pydantic import BaseModel
from datetime import datetime

class MessageRead(BaseModel):
    id: int
    user_id: int
    role: str
    content: str
    timestamp: datetime

    model_config = {
        "from_attributes": True  # replaces orm_mode = True
    }

class MessageCreate(BaseModel):
    user_id: int
    username: str | None = None  # optional if creating new user
    role: str
    content: str
