from app.repos.message_history_repo import MessageRepository
from app.schemas.message_history_schemas import MessageRead

class ChatService:
    def __init__(self, message_repo: MessageRepository):
        self.message_repo = message_repo

    def save_user_message(self, user_id: int, content: str):
        # Save user message
        user_message = self.message_repo.save_message(user_id, "user", content)
        return MessageRead.from_orm(user_message)

    def get_history(self, user_id: int, limit: int = 10):
        # Return the most recent N user messages
        history = self.message_repo.get_messages_for_user(user_id, limit=limit)
        return [MessageRead.from_orm(m) for m in history]

