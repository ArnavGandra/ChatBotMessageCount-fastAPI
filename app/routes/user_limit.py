"""
API endpoints for messaging.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import message_history_schemas
from ..services import message_history
from ..exceptions import LimitExceededException
from ..utils.dependencies import get_db
from app.schemas.user_limit_schemas import MessageResponse

router = APIRouter()

@router.post(
    "/send/{user_id}",
    response_model=MessageResponse,
    summary="Send a message",
    description="Consumes one message quota. Users can send up to 20 messages per 12 hours."
)
def send_message(user_id: str, db: Session = Depends(get_db)):
    """
    Endpoint to handle user message.
    - Validates quota
    - Updates count
    - Returns usage info
    """
    try:
        user = process_message(db, user_id)
        return MessageResponse(
            success=True,
            message="Message accepted.",
            usage=f"{user.message_count}/{20}"
        )
    except LimitExceededException as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Message limit exceeded. Please wait {e.wait_hours} hours."
        )
