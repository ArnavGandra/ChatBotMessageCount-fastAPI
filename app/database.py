"""
Database configuration module.
Defines SQLAlchemy engine, session and base for models.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:eAIpassword@database-1.c3y4gguq0fev.us-east-2.rds.amazonaws.com/eai_db")

# Engine connects SQLAlchemy to Postgres
engine = create_engine(DATABASE_URL)

# Session factory (used in request lifecycle)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()