from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

# Pydantic schema for TestRequest validation
class TestRequestSchema(BaseModel):
    request_id: int
    doctor_id: int
    patient_id: int
    center_id: int
    name: str = Field(..., min_length=1, max_length=100)
    test_details: str = Field(..., min_length=1, max_length=500)
    status: str = Field(..., min_length=1, max_length=50)

# POST route to add a test request
@router.post("/test_requests", response_model=TestRequestSchema, status_code=status.HTTP_201_CREATED)
def add_test_request(test_request: TestRequestSchema, db: Session = Depends(get_db)):
    existing_request = db.query(models.TestRequest).filter(models.TestRequest.request_id == test_request.request_id).first()
    if existing_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Test request already exists")
    new_request = models.TestRequest(
        request_id=test_request.request_id,
        doctor_id=test_request.doctor_id,
        patient_id=test_request.patient_id,
        center_id=test_request.center_id,
        name=test_request.name,
        test_details=test_request.test_details,
        status=test_request.status
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

# GET route to retrieve a test request by request_id
@router.get("/test_requests/{request_id}", response_model=TestRequestSchema, status_code=status.HTTP_200_OK)
def get_test_request(request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(models.TestRequest).filter(models.TestRequest.request_id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test request not found")
    return db_request
