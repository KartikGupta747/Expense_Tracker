from sqlalchemy.orm import Session
from app import models, schemas
from app.security import get_password_hash
from typing import Optional
from datetime import date

def get_user_by_email(db: Session, email: str):
    """Fetches a user from the database by their email."""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Hashes the password and saves a new user to the database."""
    hashed_password = get_password_hash(user.password)
    
    # Create the database model instance
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password
    )
    
    # Add to session, save to DB, and refresh to get the generated ID
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


# --- CATEGORY CRUD ---

def create_category(db: Session, category: schemas.CategoryCreate, user_id: int):
    """Creates a new category for a specific user."""
    db_category = models.Category(**category.model_dump(), user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories_by_user(db: Session, user_id: int):
    """Fetches all categories belonging to a specific user."""
    return db.query(models.Category).filter(models.Category.user_id == user_id).all()


# --- EXPENSE CRUD ---

def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    """Logs a new expense for a specific user."""
    db_expense = models.Expense(**expense.model_dump(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses_by_user(
    db: Session, 
    user_id: int, 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None,
    category_id: Optional[int] = None
):
    """
    Fetches expenses for a user. 
    Includes optional filters for date ranges and specific categories.
    """
    query = db.query(models.Expense).filter(models.Expense.user_id == user_id)
    
    # Apply optional filters if the user requested them
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)
    if category_id:
        query = query.filter(models.Expense.category_id == category_id)
        
    return query.all()