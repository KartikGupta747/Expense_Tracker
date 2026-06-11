# this file defines the Pydantic schemas for our API. Schemas are used to validate and serialize/deserialize data. They help ensure that the data we receive from the user is in the correct format.

from pydantic import BaseModel, EmailStr
from datetime import datetime

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