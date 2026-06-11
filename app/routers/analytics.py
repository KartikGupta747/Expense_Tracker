import csv
import io
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app import crud, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics & Reports"])

@router.get("/monthly")
def get_monthly_insights(
    year: int, 
    month: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Returns total spent, average per day, and highest expense for the month."""
    summary = crud.get_monthly_summary(db=db, user_id=current_user.id, year=year, month=month)
    breakdown = crud.get_spending_by_category(db=db, user_id=current_user.id, year=year, month=month)
    
    # Format the breakdown cleanly for the frontend
    category_totals = {item.name: item.total_spent for item in breakdown}
    
    return {
        "summary": summary,
        "breakdown": category_totals
    }

@router.get("/export")
def export_expenses_csv(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Generates a downloadable CSV file of all user expenses."""
    # 1. Fetch all expenses for this user
    expenses = crud.get_expenses_by_user(db=db, user_id=current_user.id)
    
    # 2. Create an in-memory string buffer
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 3. Write the CSV headers
    writer.writerow(["Date", "Amount", "Description", "Category ID"])
    
    # 4. Write the data rows
    for expense in expenses:
        writer.writerow([expense.date, expense.amount, expense.description, expense.category_id])
    
    # 5. Create a response that forces the browser to download a file
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=expense_report.csv"
    
    return response