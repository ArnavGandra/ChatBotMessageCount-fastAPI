"""
FastAPI entry point.
Initializes application, database, and routes.
"""

from fastapi import FastAPI
from .database import Base, engine
from .routes import messages

# Create tables (safe for small projects; use Alembic for migrations in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Messaging API",
    description="API for enforcing user message limits (20 per 12 hours).",
    version="1.0.0"
)

# Register routers
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
