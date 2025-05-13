from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session
from app.dependencies.db_session_dependency import get_session
from app.models.user import User
from passlib.context import CryptContext
from app.routers.api_response.custom_api_response import CustomApiSuccessResponse

# This module defines the API routes for user-related operations.
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): The password to hash.
    
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

class BaseUser(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: str | None = Field(default=None, min_length=10, max_length=100)


class UserIn(BaseUser):
    password: str


@router.post("/register", response_model=BaseUser, response_class=CustomApiSuccessResponse, status_code=201)
async def create_user(user: UserIn, session: Session = Depends(get_session)) -> BaseUser:
    """
    Create a new user.
    
    Args:
        user (UserIn): The user data to create.
    
    Returns:
        BaseUser: The created user data.
    """
    
    if User.email_exists(session, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    
    hashed_password = hash_password(user.password)
    
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
        address=user.address
    )
    
    
    new_user.save(session)
    
    return user


