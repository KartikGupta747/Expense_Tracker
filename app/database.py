from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# 1. Create the SQLAlchemy engine using the validated database URL from our .env file
engine = create_engine(settings.DATABASE_URL)

# 2. Create a SessionLocal class. Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create a Base class. Later, all our database tables will inherit from this class.
Base = declarative_base()

# 4. Dependency to get a database session for each API request, ensuring connections close cleanly.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()