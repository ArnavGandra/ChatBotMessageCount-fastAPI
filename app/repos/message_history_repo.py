from sqlalchemy.orm import Session
from app.models.message_history import Message  # your actual model

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, user_id: int, role: str, content: str):
        message = Message(user_id=user_id, role=role, content=content)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_for_user(self, user_id: int, limit: int = 20):
        messages = (
            self.db.query(Message)  # ✅ use Message model, not message_history
            .filter(Message.user_id == user_id)
            .order_by(Message.timestamp.desc())
            .limit(limit)
            .all()
        )
        return list(reversed(messages))  # chronological order

