from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/business", tags=["business"])

@router.get("/")
def list_businesses(db: Session = Depends(get_db)):
    return db.query(models.Business).all()


@router.get("/{business_id}")
def get_business(business_id: str, db: Session = Depends(get_db)):
    return db.query(models.Business).filter(models.Business.id == business_id).first()
