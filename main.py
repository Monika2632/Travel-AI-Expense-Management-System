from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil

# Database & models
from database import engine
from models import users, expenses

# Auth
from auth import hash_password, verify_password, create_token

# Services
from services.ai_parser import extract_receipt
from services.policy_engine import validate

# Pydantic models
from pydantic import BaseModel
from typing import Optional

# SQLAlchemy
from sqlalchemy import func, select

# Initialize FastAPI app
app = FastAPI()

# =========================
# 🌐 CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📦 REQUEST MODELS
# =========================

class RegisterRequest(BaseModel):
    name: str
    password: str
    role: str

class LoginRequest(BaseModel):
    name: str
    password: str

class ConfirmRequest(BaseModel):
    user_id: int
    role: str
    amount: float
    type: str
    gst: Optional[float] = 0
    vendor: Optional[str] = None
    date: Optional[str] = None

# =========================
# 🏠 HOME API
# =========================
@app.get("/")
def home():
    return {"message": "Travel AI Expense System Running 🚀"}

# =========================
# 🔑 REGISTER API
# =========================
@app.post("/register")
def register(data: RegisterRequest):
    with engine.connect() as conn:
        conn.execute(users.insert().values(
            name=data.name,
            password=hash_password(data.password),
            role=data.role
        ))
        conn.commit()

    return {"message": "User registered successfully"}

# =========================
# 🔐 LOGIN API
# =========================
@app.post("/login")
def login(data: LoginRequest):
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()

    if not result:
        return {"error": "No user registered"}

    for user in result:
        if user.name == data.name and verify_password(data.password, user.password):
            token = create_token({
                "user_id": user.id,
                "role": user.role
            })
            return {"token": token}

    return {"error": "Invalid username or password"}

# =========================
# 📤 UPLOAD RECEIPT
# =========================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        file_path = f"uploads/{file.filename}"

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract data
        extracted_data = extract_receipt(file_path)

        return {
            "message": "Receipt processed successfully",
            "extracted_data": extracted_data
        }

    except Exception as e:
        return {
            "error": "Internal Server Error",
            "details": str(e)
        }

# =========================
# ✅ CONFIRM EXPENSE (FIXED)
# =========================
@app.post("/confirm")
def confirm(data: ConfirmRequest):
    role = data.role
    amount = float(data.amount)
    gst = float(data.gst or 0)
    expense_type = data.type

    # ✅ ADD TAX
    total_amount = amount + gst

    is_valid = validate(role, expense_type, amount)

    with engine.connect() as conn:
        if is_valid:
            conn.execute(
                expenses.insert().values(
                    user_id=data.user_id,
                    type=expense_type,
                    amount=total_amount,   # ✅ FIXED (amount + gst)
                    gst=gst,              # ✅ store tax separately
                    vendor=data.vendor or "",
                    date=data.date or "",
                    status="approved"
                )
            )
            conn.commit()

            return {
                "status": "approved",
                "message": "Expense saved",
                "total_amount": total_amount
            }

    return {"status": "rejected", "message": "Policy violation"}

# =========================
# 📊 ANALYTICS API (IMPROVED)
# =========================
@app.get("/analytics")
def get_analytics():
    with engine.connect() as conn:

        total = conn.execute(
            select(func.sum(expenses.c.amount))
        ).scalar()

        travel = conn.execute(
            select(func.sum(expenses.c.amount))
            .where(expenses.c.type == "travel")
        ).scalar()

        taxi = conn.execute(
            select(func.sum(expenses.c.amount))
            .where(expenses.c.type == "taxi")
        ).scalar()

        hotel = conn.execute(
            select(func.sum(expenses.c.amount))
            .where(expenses.c.type == "hotel")
        ).scalar()

    return {
        "total_expense": total or 0,
        "travel_expense": travel or 0,
        "taxi_expense": taxi or 0,
        "hotel_expense": hotel or 0
    }