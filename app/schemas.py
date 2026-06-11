# this file defines the Pydantic schemas for our API. Schemas are used to validate and serialize/deserialize data. They help ensure that the data we receive from the user is in the correct format.

from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

# 1. What we expect from the user when they sign up
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# 2. What we return to the user (notice we DO NOT return the password!)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # Tells Pydantic to read data even if it's an SQLAlchemy model

# --- CATEGORY SCHEMAS ---
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    user_id: int

    class Config:
        from_attributes = True

# --- EXPENSE SCHEMAS ---
class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category_id: int
    date: date

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str
    date: date
    category_id: int
    user_id: int

    class Config:
        from_attributes = True

# --- BUDGET SCHEMAS ---
class BudgetCreate(BaseModel):
    category_id: int
    monthly_limit: float

class BudgetResponse(BaseModel):
    id: int
    category_id: int
    user_id: int
    monthly_limit: float

    class Config:
        from_attributes = True