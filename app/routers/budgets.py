from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("/", response_model=schemas.BudgetResponse)
def set_budget(
    budget: schemas.BudgetCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Sets or updates a monthly budget limit for a specific category."""
    return crud.set_budget(db=db, budget=budget, user_id=current_user.id)

@router.get("/", response_model=List[schemas.BudgetResponse])
def get_budgets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Fetches all budget limits set by the user."""
    return crud.get_budgets_by_user(db=db, user_id=current_user.id)