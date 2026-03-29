from sqlalchemy import create_engine
from models import metadata

# SQLite database file
engine = create_engine("sqlite:///db.sqlite3")

# Create tables
metadata.create_all(engine)