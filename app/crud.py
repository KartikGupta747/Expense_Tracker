from sqlalchemy.orm import Session
from app import models, schemas
from app.security import get_password_hash
from typing import Optional
from datetime import date
from sqlalchemy import func, extract
from calendar import monthrange

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

# --- BUDGET CRUD ---

def set_budget(db: Session, budget: schemas.BudgetCreate, user_id: int):
    """
    Sets a monthly budget for a category. 
    If a budget already exists for this category, it updates the limit.
    """
    existing_budget = db.query(models.Budget).filter(
        models.Budget.user_id == user_id,
        models.Budget.category_id == budget.category_id
    ).first()

    if existing_budget:
        existing_budget.monthly_limit = budget.monthly_limit
        db.commit()
        db.refresh(existing_budget)
        return existing_budget
    else:
        new_budget = models.Budget(**budget.model_dump(), user_id=user_id)
        db.add(new_budget)
        db.commit()
        db.refresh(new_budget)
        return new_budget

def get_budgets_by_user(db: Session, user_id: int):
    """Fetches all budgets for a user."""
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()


# --- ANALYTICS CRUD ---

def get_monthly_summary(db: Session, user_id: int, year: int, month: int):
    """
    Runs SQL aggregations to calculate total spent, average per day, 
    and finds the highest single expense for a specific month.
    """
    # 1. Base query filtered by user, year, and month
    base_query = db.query(models.Expense).filter(
        models.Expense.user_id == user_id,
        extract('year', models.Expense.date) == year,
        extract('month', models.Expense.date) == month
    )
    
    # 2. Calculate Total Spent
    total_spent = base_query.with_entities(func.sum(models.Expense.amount)).scalar() or 0.0
    
    # 3. Calculate Highest Single Expense
    highest_expense = base_query.with_entities(func.max(models.Expense.amount)).scalar() or 0.0
    
    # 4. Calculate Average Per Day
    _, num_days = monthrange(year, month)
    avg_per_day = round(total_spent / num_days, 2)
    
    return {
        "total_spent": total_spent,
        "average_per_day": avg_per_day,
        "highest_expense": highest_expense
    }

def get_spending_by_category(db: Session, user_id: int, year: int, month: int):
    """
    Joins Expenses and Categories to group spending.
    Equivalent to: SELECT category.name, SUM(amount) FROM expenses ... GROUP BY category.name
    """
    return db.query(
        models.Category.name,
        func.sum(models.Expense.amount).label("total_spent")
    ).join(models.Expense, models.Category.id == models.Expense.category_id)\
     .filter(
        models.Expense.user_id == user_id,
        extract('year', models.Expense.date) == year,
        extract('month', models.Expense.date) == month
     ).group_by(models.Category.name).all()