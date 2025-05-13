from sqlmodel import Session
from app.database.connection.sql_connection import engine

def get_session():
    """
    Create and yield a SQLModel Session.
    
    This function is designed to be used as a FastAPI dependency.
    The session is automatically closed after the request is processed.
    """
    with Session(engine) as session:
        yield session