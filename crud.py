from sqlalchemy.orm import Session
import random
from datetime import datetime, timedelta
from passlib.context import CryptContext # type: ignore
from models import User
import schemas
import pyotp  # type: ignore
import random
from sqlalchemy.orm import Session
from models import Subscription
from schemas import SubscriptionCreate, SubscriptionUpdate,SubscriptionPurchaseSchema
from fastapi import Depends,HTTPException,status
from database import get_db
import models


# Generate OTP

def generate_otp():
    # Generate a 4-digit random number
    otp = random.randint(1000, 9999)
    return otp





'''# Create user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        mobile=user.mobile,
        profession=user.profession,
        city=user.city,
        role="user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user'''

# Get user by mobile (for OTP-based login)
def get_user_by_mobile(db: Session, mobile: str):
    return db.query(models.User).filter(models.User.mobile == mobile).first()

# Update OTP and OTP expiration for user
def update_otp(db: Session, mobile: str, otp: str):
    db_user = db.query(models.User).filter(models.User.mobile == mobile).first()
    if db_user:
        db_user.otp = otp
        db_user.otp_expiry = (datetime.utcnow() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')  # OTP expires in 5 minutes
        db.commit()
        db.refresh(db_user)
    return db_user


def verify_otp(db: Session, mobile: str, otp: str):
    db_user = db.query(models.User).filter(models.User.mobile == mobile).first()
    if db_user and db_user.otp == otp:
        # Check if OTP is expired
        if datetime.utcnow() < db_user.otp_expiry:
            # Set OTP to NULL after successful login
            db_user.otp = None
            db_user.otp_expiry = None  # Clear OTP expiry as well
            db.commit()
            db.refresh(db_user)  # Refresh the instance with the updated database state
            return db_user  # OTP is valid
    return None  # Invalid OTP or expired


# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Update admin profile
def update_admin(db: Session, updates: schemas.AdminUpdate):
    db_admin = db.query(models.User).filter(models.User.role == "admin").first()
    if not db_admin:
        return None
    
    if updates.username:
        db_admin.username = updates.username
    if updates.email:
        db_admin.email = updates.email
    if updates.mobile:
        db_admin.mobile = updates.mobile
    if updates.profession:
        db_admin.profession = updates.profession
    if updates.city:
        db_admin.city = updates.city
    if updates.subscription_type:
        db_admin.subscription_type = updates.subscription_type

    db.commit()
    db.refresh(db_admin)
    return db_admin

# Update user profile
def update_user(db: Session, user_id: int, updates: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id, models.User.role == "user").first()
    if not db_user:
        return None

    # Update only provided fields
    if updates.email is not None:
        db_user.email = updates.email
    if updates.mobile is not None:
        db_user.mobile = updates.mobile
    if updates.profession is not None:
        db_user.profession = updates.profession
    if updates.city is not None:
        db_user.city = updates.city

    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(
    subscription_data: SubscriptionPurchaseSchema,  # Extract mobile from the body schema
    db: Session = Depends(get_db)
) -> User:
    """
    Fetch the current user based on the mobile number provided in the request body.
    """
    db_user = db.query(User).filter(User.mobile == subscription_data.mobile).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user
