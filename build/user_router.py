from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
import models
from datetime import datetime

router = APIRouter()

# Pydantic schema for user validation
class Userschema(BaseModel):
    user_id: int
    role: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str = Field(..., min_length=8)
    contact_info: str = Field(min_length=10)
    registration_date: datetime = Field(None)

# POST route to add a user
@router.post("/users", response_model=Userschema, status_code=status.HTTP_201_CREATED)
def add_user(user: Userschema, db: Session = Depends(get_db)):
    existing_user = db.query(models.USER).filter(models.USER.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user = models.USER(
        role=user.role,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
        contact_info=user.contact_info,
        registration_date=user.registration_date or datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# PUT route to update user information
@router.put("/users/{user_id}", response_model=Userschema, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: Userschema, db: Session = Depends(get_db)):
    existing_user = db.query(models.USER).filter(models.USER.user_id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    existing_user.first_name = user.first_name
    existing_user.last_name = user.last_name
    existing_user.email = user.email
    existing_user.password = user.password
    existing_user.contact_info = user.contact_info
    existing_user.registration_date = user.registration_date or datetime.now()

    db.commit()
    db.refresh(existing_user)
    return existing_user
