from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserBase, Token, UserUpdate,UserUpdateProfile
from app.utils.auth import create_access_token, verify_password, hash_password, get_current_user, get_current_active_user
from datetime import timedelta
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to the User Management Service!"}

@router.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon available"}


# Token Endpoint
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()  # Using email for login
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",  
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)  # Using email for token
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    db_user = db.query(User).filter(User.email == user.email).first()  # Using email check for existing users
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,  # Optional username, kept for backward compatibility
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role="user",  # Default role
        public_address=user.public_address  # Storing wallet address
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Account created successfully. Please log in."}



@router.post("/users/", status_code=status.HTTP_201_CREATED)
def admin_create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create new users with roles")

    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role  # Now, the role is properly passed from the request body
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully by admin", "username": new_user.username, "role": new_user.role}





@router.get("/users/", response_model=list[UserBase])
async def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["admin", "moderator"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    users = db.query(User).all()
    return users

@router.put("/users/me", response_model=dict)
async def update_current_user(
    updated_user: UserUpdateProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Fetch user from the database
    user = db.query(User).filter(User.id == current_user.id).first()

    # Check for conflicts when updating email or username
    if updated_user.email and updated_user.email != user.email:
        if db.query(User).filter(User.email == updated_user.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    if updated_user.username and updated_user.username != user.username:
        if db.query(User).filter(User.username == updated_user.username).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    # Update fields
    if updated_user.username:
        user.username = updated_user.username
    if updated_user.email:
        user.email = updated_user.email
    if updated_user.full_name:
        user.full_name = updated_user.full_name
    if updated_user.password:
        user.hashed_password = hash_password(updated_user.password)  # Hash new password
    if updated_user.public_address:
        user.public_address = updated_user.public_address  # Update wallet address

    db.commit()
    db.refresh(user)

    return {"message": "User profile updated successfully"}

@router.delete("/users/me", response_model=dict)
async def delete_current_user(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Delete the user from the database
    db.query(User).filter(User.id == current_user.id).delete()
    db.commit()
    return {"message": "User account deleted successfully"}

@router.get("/users/", response_model=list[UserBase])
async def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role not in ["admin", "moderator"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    users = db.query(User).all()
    return users


@router.put("/users/{user_id}/activate", response_model=dict)
async def activate_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can activate users")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.disabled = False
    db.commit()
    return {"message": f"User {user.username} activated successfully"}

@router.put("/users/{user_id}/deactivate", response_model=dict)
async def deactivate_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can deactivate users")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.disabled = True
    db.commit()
    return {"message": f"User {user.username} deactivated successfully"}


