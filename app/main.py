from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.routers import auth

app = FastAPI(
    title="Expense Tracker API",
    description="Production-grade personal finance backend",
    version="1.0.0"
)
app.include_router(auth.router)

@app.get("/health", tags=["Health Check"])
def health_check(db: Session = Depends(get_db)):
    """
    Verifies that the API is up and can connect to the database.
    """
    try:
        # Run a simple query to verify the database connection is live
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        # If the connection fails, it will return the exact error message
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}