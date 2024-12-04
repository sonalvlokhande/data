import random
from datetime import datetime, timedelta,timezone
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from passlib.context import CryptContext  # type: ignore


# Password encryption setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database session
db: Session = SessionLocal()

def generate_otp():
    """Generate a random 6-digit OTP"""
    otp = random.randint(100000, 999999)
    return str(otp)

# Generate OTP for admin user
otp = generate_otp()  # Call the function to generate OTP
otp_expiry = datetime.utcnow() + timedelta(minutes=10)  # OTP expiry time (10 minutes from now)

# Create admin user
admin = User(
    username="admin",
    email="admin@gmail.com",
    mobile="9875645678",
    profession="Admin",
    city="Pune",
    role="admin",  # Explicit role for admin
    subscription_name="premium",  # Explicit subscription for admin
    otp=otp,  # Store the OTP
    otp_expiry=otp_expiry  # Store the OTP expiry time
)

try:
    # Add and commit to the database
    db.add(admin)
    db.commit()
    print("Admin user created successfully.")
except Exception as e:
    db.rollback()
    print(f"Error creating admin user: {e}")
finally:
    db.close()
