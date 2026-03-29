from jose import jwt
from datetime import datetime, timedelta
import bcrypt

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

# 🔒 Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# 🔑 Verify password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# 🎟️ Create JWT token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=2)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)