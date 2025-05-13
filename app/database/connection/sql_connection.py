# This module handles the SQL database connection and session management for the application.
# It uses SQLModel to create an engine and session for interacting with the database.

from sqlmodel import create_engine, SQLModel, Session
from app.models import *
from app.configs.database import DatabaseSettings


db_settings = DatabaseSettings()

engine = create_engine(db_settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    """
    Create the database and tables if they do not exist.
    """
    
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Create and yield a SQLModel Session.
    
    This function is designed to be used as a FastAPI dependency.
    The session is automatically closed after the request is processed.
    """
    with Session(engine) as session:
        yield session
    

