from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repos import message_history_repo
from app.schemas import message_history_schemas
from app.schemas.message_history_schemas import MessageRead, MessageCreate
from app.repos.message_history_repo import MessageRepository
from app.models.message_history import User, Message
from typing import List
from fastapi import HTTPException

router = APIRouter()

@router.post("/save-message", response_model=MessageRead)
def save_message(msg: MessageCreate, db: Session = Depends(get_db)):
    """
    Receives a message from the frontend (user or AI) and saves it in the DB.
    If the user does not exist, it will create a new user with the given username.
    """

    # Check if user exists
    user = db.query(User).filter(User.id == msg.user_id).first()
    if not user:
        if not msg.username:
            raise HTTPException(status_code=400, detail="Username required for new user")
        user = User(id=msg.user_id, username=msg.username)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Save the message
    repo = MessageRepository(db)
    message = repo.save_message(user_id=user.id, role=msg.role, content=msg.content)

    return MessageRead.from_orm(message)

@router.get("/history/{user_id}", response_model=List[MessageRead])
def get_message_history(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    repo = MessageRepository(db)
    messages = repo.get_messages_for_user(user_id)
    return [MessageRead.from_orm(m) for m in messages]