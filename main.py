from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from pydantic import BaseModel

app = FastAPI()

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="connect/templates")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for user update
class UserUpdate(BaseModel):
    role:str
    first_name: str
    last_name: str
    email: str
    contact_info: str

@app.get("/users/")
async def get_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    # Fetch the user to update
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user details
    user.first_name = user_update.first_name
    user.last_name = user_update.last_name
    user.email = user_update.email
    user.contact_info = user_update.contact_info
    
    db.commit()  # Commit the changes to the database
    db.refresh(user)  # Refresh the instance to reflect changes
    
    return {"message": "User updated successfully", "user": user}

