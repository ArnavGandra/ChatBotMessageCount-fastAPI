"""
Shared dependencies for FastAPI routes.
"""

from ..database import SessionLocal
from sqlalchemy.orm import Session

def get_db():
    """Provide a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
