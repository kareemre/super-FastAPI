from app.models.base import (
    Base, Optional, List, datetime, TYPE_CHECKING, 
    Mapped, mapped_column, ForeignKey, Integer, String, DateTime, relationship
)
from sqlalchemy import select

if TYPE_CHECKING:
    from app.models.order import Order  

class User(Base):
    __tablename__ = "users"

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @classmethod
    async def get_user_by_email(cls, session, email: str):
        
        stmt = select(cls).where(cls.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def email_exists(cls, session, email: str) -> bool:
        user = await cls.get_user_by_email(session, email)
        return user is not None
    
    
    @classmethod
    async def create_user(cls, session, **kwargs) -> "User":
        """
        Create a new user and save to database.
        
        Args:
            session: Async database session
            **kwargs: User data fields
            
        Returns:
            Created user instance
        """
        user = cls(**kwargs)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def save(self, session) -> "User":
        """
        Save the current user instance to database.
        
        Args:
            session: Async database session
            
        Returns:
            The saved user instance
        """
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self
    
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"