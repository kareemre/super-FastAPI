# here is a user.py model using SQLModel, defining all users' database operations here following active record pattern
#for shared heavy queries we will use the repository package 

from app.models.base import SQLModel, Field, Relationship, Optional, List, datetime, TYPE_CHECKING
from sqlmodel import Session, select



class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    phone: str
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
   
    
    @classmethod
    def get_user_by_email(cls, session: Session, email: str):
        """
        Get a user by email.
        
        Args:
            email (str): The email of the user to retrieve.
        
        Returns:
            User: The user with the specified email.
        """
        return session.exec(
            select(cls).where(cls.email == email)
        ).first()
    
    @classmethod
    def email_exists(cls, session: Session, email: str) -> bool:
        """
        Check if a user with the specified email exists.
        
        Args:
            email (str): The email to check.
        
        Returns:
            bool: True if the email exists, False otherwise.
        """
        return cls.get_user_by_email(session, email) is not None
    
    def save(self, session: Session):
        """
        Save the user to the database.
        
        Args:
            session (Session): The SQLModel session to use.
        
        :Returns:
            User: The saved user instance.
        """
        session.add(self)
        session.commit()
        session.refresh(self)
        
        return self