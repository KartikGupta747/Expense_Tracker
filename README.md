# Expense Tracker API

*A production-ready RESTful backend built with FastAPI for personal expense management, featuring JWT authentication, category-wise budgeting, spending analytics, CSV report export, and PostgreSQL persistence.*

## Overview

Expense Tracker API is a backend service that enables users to securely manage their personal finances. The application provides authentication, expense categorization, monthly budgeting, analytics, and report generation through REST APIs.

The project follows a modular architecture by separating routers, business logic, database models, validation schemas, authentication, and dependencies. SQLAlchemy ORM is used for persistence, Alembic handles schema migrations, and JWT secures protected endpoints.

The application demonstrates backend engineering concepts commonly expected in production systems:

* JWT Authentication
* REST API Design
* SQLAlchemy ORM
* PostgreSQL
* Alembic Database Migrations
* Pydantic Validation
* Dependency Injection
* Modular FastAPI Architecture
* Analytics using SQL Aggregations
* CSV Report Generation

---

# Features

## Authentication

* User Registration
* User Login
* Secure Password Hashing using bcrypt
* JWT Token Generation
* Protected Routes
* Current User Dependency Injection

---

## Expense Management

* Create expenses
* View all expenses
* Filter by

  * Date Range
  * Category
* Store description
* Track amount
* Track transaction date

---

## Category Management

* Create custom categories
* Retrieve user-specific categories
* Categories isolated per user

---

## Budget Management

* Set monthly budget
* Update existing budget
* Retrieve budgets
* Budget maintained category-wise

---

## Analytics

Monthly analytics include:

* Total spending
* Average spending per day
* Highest expense
* Category-wise spending

Implemented using SQLAlchemy aggregation functions:

* SUM()
* MAX()
* GROUP BY
* EXTRACT()

---

## Report Generation

Generate downloadable CSV reports containing:

* Expense Date
* Amount
* Description
* Category

---

# Tech Stack

| Layer              | Technology                        |
| ------------------ | --------------------------------- |
| Backend            | FastAPI                           |
| Language           | Python                            |
| Database           | PostgreSQL                        |
| ORM                | SQLAlchemy 2.0                    |
| Validation         | Pydantic v2                       |
| Authentication     | JWT (python-jose)                 |
| Password Hashing   | bcrypt / passlib                  |
| Database Migration | Alembic                           |
| Environment Config | python-dotenv / pydantic-settings |
| API Testing        | Swagger UI                        |

---

# Architecture

```text
                 Client
                    │
          HTTP REST Requests
                    │
            FastAPI Application
                    │
      ┌─────────────┼─────────────┐
      │             │             │
 Authentication  Expense APIs  Analytics APIs
      │             │             │
      └─────────────┼─────────────┘
                    │
             CRUD Layer
                    │
              SQLAlchemy ORM
                    │
             PostgreSQL Database
```

---

# Project Structure

```text
Expense_Tracker/
│
├── alembic/
│   ├── env.py
│   ├── versions/
│   └── script.py.mako
│
├── app/
│   ├── routers/
│   │     ├── auth.py
│   │     ├── categories.py
│   │     ├── expenses.py
│   │     ├── budgets.py
│   │     └── analytics.py
│   │
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── main.py
│
├── requirements.txt
├── alembic.ini
└── README.md
```

---

# Folder Explanation

### `main.py`

Application entry point.

Responsibilities:

* Creates FastAPI instance
* Registers routers
* Health endpoint
* CSV export endpoint
* Application metadata

---

### `routers/`

Contains all REST endpoints.

Each router handles a single business domain.

```
auth.py
```

Handles

* Register
* Login

---

```
categories.py
```

Handles

* Create Category
* Get Categories

---

```
expenses.py
```

Handles

* Add Expense
* Get Expenses
* Filtering

---

```
budgets.py
```

Handles

* Set Budget
* View Budget

---

```
analytics.py
```

Handles

* Monthly Summary
* Category-wise Spending

---

### `crud.py`

Business Logic Layer.

Instead of placing SQL inside routers, every database operation is abstracted into CRUD functions.

Examples include:

* create_user()
* create_category()
* create_expense()
* get_expenses_by_user()
* set_budget()
* get_monthly_summary()
* get_spending_by_category()

This separation keeps routers lightweight and improves maintainability.

Excellent. Yeh **Part 2** hai. Is section ke baad README almost production quality ho jayega.

---

# Database Design

The application follows a relational database model where every user owns their categories, expenses, and budgets.

## Entity Relationship Diagram

```mermaid
erDiagram

USER ||--o{ CATEGORY : owns
USER ||--o{ EXPENSE : creates
USER ||--o{ BUDGET : sets

CATEGORY ||--o{ EXPENSE : categorizes
CATEGORY ||--|| BUDGET : budget_for

USER {
    int id PK
    string name
    string email
    string password_hash
}

CATEGORY {
    int id PK
    string name
    int user_id FK
}

EXPENSE {
    int id PK
    float amount
    string description
    date date
    int category_id FK
    int user_id FK
}

BUDGET {
    int id PK
    float monthly_limit
    int category_id FK
    int user_id FK
}
```

---

# Database Relationships

## User

Stores account information.

### Fields

| Field         | Description            |
| ------------- | ---------------------- |
| id            | Primary Key            |
| name          | User Name              |
| email         | Unique Email           |
| password_hash | bcrypt Hashed Password |

Relationships

```
One User
    ├── Many Categories
    ├── Many Expenses
    └── Many Budgets
```

---

## Category

Represents an expense category.

Examples

```
Food

Travel

Shopping

Rent

Entertainment
```

Each category belongs to only one user.

---

## Expense

Stores every financial transaction.

Fields

```
Amount

Description

Transaction Date

Category

Owner
```

Every expense references

* User
* Category

---

## Budget

Stores spending limits.

Each record links

```
User
↓

Category
↓

Monthly Limit
```

When the user updates a budget, the existing record is updated instead of creating duplicates.

---

# Authentication Flow

Authentication is implemented using JWT access tokens.

```mermaid
sequenceDiagram

participant Client
participant FastAPI
participant Database
participant JWT

Client->>FastAPI:Register
FastAPI->>Database:Store hashed password
Database-->>FastAPI:User Created
FastAPI-->>Client:Success

Client->>FastAPI:Login
FastAPI->>Database:Verify Email
Database-->>FastAPI:User

FastAPI->>JWT:Generate Access Token

JWT-->>FastAPI:Token

FastAPI-->>Client:JWT Token

Client->>FastAPI:Protected API
FastAPI->>JWT:Validate Token
JWT-->>FastAPI:Current User
FastAPI-->>Client:Requested Data
```

---

# Password Security

Passwords are **never stored directly**.

Registration flow

```
Plain Password
        │
        ▼
bcrypt Hashing
        │
        ▼
Database
```

Login flow

```
Entered Password

↓

bcrypt verify()

↓

Hash Match

↓

JWT Generated
```

---

# JWT Workflow

```
User Login

↓

Verify Credentials

↓

Generate JWT

↓

Return Token

↓

Authorization Header

↓

Bearer <token>

↓

Protected Route

↓

Decode Token

↓

Current User
```

---

# Request Lifecycle

Every authenticated request follows the same execution pipeline.

```mermaid
flowchart TD

A[Client Request]

-->B[Router]

-->C[JWT Authentication]

-->D[Dependency Injection]

-->E[CRUD Layer]

-->F[SQLAlchemy ORM]

-->G[PostgreSQL]

-->H[Response]
```

---

# Dependency Injection

FastAPI dependencies are used to automatically provide

* Database Session
* Authenticated User

Example flow

```
Endpoint

↓

Depends(get_db)

↓

Database Session
```

and

```
Endpoint

↓

Depends(get_current_user)

↓

JWT Verification

↓

Current User
```

Routers therefore never manually create database connections.

---

# Business Logic Separation

The project follows a layered architecture.

```
Router

↓

CRUD

↓

SQLAlchemy

↓

Database
```

### Router Layer

Responsible for

* Receiving HTTP Requests
* Validation
* Returning Responses

Contains **no SQL logic**.

---

### CRUD Layer

Responsible for

* Database Queries
* Updates
* Inserts
* Aggregations

Every database interaction is centralized inside `crud.py`.

---

### Database Layer

Responsible for

* Model Mapping
* Relationships
* Transactions

SQLAlchemy converts ORM objects into SQL queries.

---

# Analytics Module

The analytics endpoint performs database-side aggregation instead of processing records in Python.

Implemented operations include:

### Total Spending

```sql
SUM(amount)
```

Purpose

```
Monthly Expense Total
```

---

### Highest Expense

```sql
MAX(amount)
```

Returns

```
Largest Transaction
```

---

### Average Per Day

Formula

```
Monthly Total

──────────────

Days in Month
```

Uses Python's `calendar.monthrange()` to correctly handle months with 28, 29, 30, or 31 days.

---

### Spending by Category

Equivalent SQL

```sql
SELECT
category.name,
SUM(expense.amount)
FROM expense
JOIN category
GROUP BY category.name;
```

Implemented using

* JOIN
* GROUP BY
* SUM
* SQLAlchemy ORM

---

# Error Handling

The API returns meaningful HTTP status codes.

| Status | Meaning               |
| ------ | --------------------- |
| 200    | Success               |
| 201    | Resource Created      |
| 400    | Invalid Request       |
| 401    | Unauthorized          |
| 404    | Resource Not Found    |
| 422    | Validation Error      |
| 500    | Internal Server Error |

---

## API Endpoints

The API follows REST principles and returns JSON responses. Authentication is performed using JWT Bearer tokens for all protected endpoints.

---

### Authentication

#### Register User

```http
POST /auth/register
```

Creates a new user account.

**Request**

```json
{
    "name": "Kartik Gupta",
    "email": "kartik@gmail.com",
    "password": "StrongPassword123"
}
```

**Response**

```json
{
    "id": 1,
    "name": "Kartik Gupta",
    "email": "kartik@gmail.com"
}
```

---

#### Login

```http
POST /auth/login
```

Authenticates a user and returns a JWT access token.

**Request**

```text
Content-Type: application/x-www-form-urlencoded

username=kartik@gmail.com
password=StrongPassword123
```

**Response**

```json
{
    "access_token": "<JWT_TOKEN>",
    "token_type": "bearer"
}
```

---

### Category APIs

#### Create Category

```http
POST /categories/
```

**Headers**

```http
Authorization: Bearer <JWT_TOKEN>
```

**Request**

```json
{
    "name": "Food"
}
```

---

#### Get Categories

```http
GET /categories/
```

Returns all categories belonging to the authenticated user.

---

### Expense APIs

#### Create Expense

```http
POST /expenses/
```

**Request**

```json
{
    "amount": 250.50,
    "description": "Dinner",
    "date": "2026-06-24",
    "category_id": 2
}
```

---

#### Get Expenses

```http
GET /expenses/
```

Supports optional query parameters.

| Parameter   | Description        |
| ----------- | ------------------ |
| start_date  | Filter from date   |
| end_date    | Filter until date  |
| category_id | Filter by category |

Example

```http
GET /expenses/?start_date=2026-06-01&end_date=2026-06-30
```

---

### Budget APIs

#### Set Budget

```http
POST /budgets/
```

**Request**

```json
{
    "category_id": 2,
    "monthly_limit": 10000
}
```

If a budget already exists for the category, it is updated instead of creating a duplicate.

---

#### Get Budgets

```http
GET /budgets/
```

Returns all budgets for the authenticated user.

---

### Analytics APIs

#### Monthly Summary

```http
GET /analytics/monthly-summary?year=2026&month=6
```

Example Response

```json
{
    "total_spent": 12450,
    "average_per_day": 415,
    "highest_expense": 3500
}
```

---

#### Category-wise Spending

```http
GET /analytics/category-summary?year=2026&month=6
```

Example Response

```json
[
    {
        "category": "Food",
        "total_spent": 4200
    },
    {
        "category": "Travel",
        "total_spent": 3150
    }
]
```

---

### Export CSV

```http
GET /export/csv
```

Downloads all expenses of the authenticated user in CSV format.

---

# Installation

## Clone Repository

```bash
git clone https://github.com/KartikGupta747/Expense_Tracker.git

cd Expense_Tracker
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL

Create a PostgreSQL database.

Example

```sql
CREATE DATABASE expense_tracker;
```

---

## Environment Variables

Create a `.env` file inside the project root.

```env
DATABASE_URL=postgresql://postgres:password@localhost/expense_tracker

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Apply Database Migrations

```bash
alembic upgrade head
```

---

## Start the Server

```bash
uvicorn app.main:app --reload
```

Server

```text
http://127.0.0.1:8000
```

---

## Interactive API Documentation

Swagger UI

```text
http://127.0.0.1:8000/docs
```

ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Example Workflow

```text
Register User
      │
      ▼
Login
      │
      ▼
Receive JWT Token
      │
      ▼
Create Categories
      │
      ▼
Add Expenses
      │
      ▼
Set Monthly Budgets
      │
      ▼
View Analytics
      │
      ▼
Export CSV Report
```

---

# Security Features

* Passwords are hashed using bcrypt before storage.
* JWT-based authentication protects private endpoints.
* SQLAlchemy ORM prevents SQL injection through parameterized queries.
* Pydantic validates request data before processing.
* Dependency injection ensures only authenticated users access protected resources.
* User data is isolated, preventing access to another user's expenses, budgets, or categories.

---

# Future Enhancements

* Expense editing and deletion
* Budget threshold notifications
* Recurring expense management
* Email reminders for budget limits
* Monthly PDF reports
* Dashboard with charts and visualizations
* Docker support
* CI/CD pipeline using GitHub Actions
* Unit and integration testing with Pytest
* Role-Based Access Control (RBAC)
* Cloud deployment on AWS, Azure, or Render
* Redis caching for analytics
* Expense receipt OCR using AI

---

# Learning Outcomes

This project demonstrates practical experience with:

* Designing RESTful APIs using FastAPI
* Implementing secure JWT authentication
* Using SQLAlchemy ORM for relational database operations
* Managing schema migrations with Alembic
* Structuring scalable backend applications with layered architecture
* Performing SQL aggregations for analytics
* Applying dependency injection in FastAPI
* Building user-specific CRUD operations
* Generating downloadable reports
* Integrating PostgreSQL with Python applications

---


