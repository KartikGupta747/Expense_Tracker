from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.CategoryResponse)
def create_category(
    category: schemas.CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # The Security Guard!
):
    """Creates a new expense category for the logged-in user."""
    return crud.create_category(db=db, category=category, user_id=current_user.id)

@router.get("/", response_model=List[schemas.CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Fetches all categories belonging to the logged-in user."""
    return crud.get_categories_by_user(db=db, user_id=current_user.id)