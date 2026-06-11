from sqlalchemy.orm import Session
from app import models, schemas
from app.security import get_password_hash

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