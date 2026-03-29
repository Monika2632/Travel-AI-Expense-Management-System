from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime
from datetime import datetime

metadata = MetaData()

# 👤 Users table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("password", String),
    Column("role", String)
)

# 💰 Expenses table
expenses = Table(
    "expenses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("type", String),        # taxi or hotel
    Column("amount", Integer),
    Column("gst", String),
    Column("vendor", String),
    Column("date", String),
    Column("status", String),      # approved/rejected
    Column("created_at", DateTime, default=datetime.utcnow)
)