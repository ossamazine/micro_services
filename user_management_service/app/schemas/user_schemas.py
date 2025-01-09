from pydantic import BaseModel, EmailStr
from enum import Enum





class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"
    
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None 

class UserBase(BaseModel):
    username: str | None = None  # Username is optional for some cases
    email: EmailStr
    full_name: str | None = None
    disabled: bool = False  # Default to False if not provided
    role: RoleEnum = RoleEnum.user
    public_address: str | None = None

class UserInDB(UserBase):
    hashed_password: str

# Schema for creating a new user
class UserCreate(BaseModel):
    username: str  # Required field
    email: EmailStr
    full_name: str | None = None
    password: str
    public_address: str  # Required field
    role: RoleEnum = RoleEnum.user  # Defaults to "user"  
    
    
class UserUpdateProfile(BaseModel):
    username: str | None = None  # Allow updating username
    email: EmailStr | None = None  # Allow updating email
    full_name: str | None = None  # Optional full name update
    password: str | None = None  # Allow updating password
    public_address: str | None = None  # Allow updating wallet address

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = None
    role: str | None = None
    public_address: str | None = None
    
    
# class UserCreate(UserBase):
#     password: str

