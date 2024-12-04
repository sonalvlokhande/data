from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DateTime
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from database import Base,engine
from sqlalchemy import Column, Integer, String, DateTime, func,Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    # Existing fields...
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    mobile = Column(String(10), unique=True)
    profession = Column(String(255))
    city = Column(String(255))
    otp = Column(String(6), nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    role = Column(String(255), default="user")
    subscription_name = Column(String(255), default="free")

    # Relationships
    active_subscription = relationship(
        "ActiveSubscription", back_populates="user", cascade="all, delete-orphan"
    )
    data_histories = relationship("DataHistory", back_populates="user")
    
    email_broadcasting = relationship(
        "EmailBroadcasting", back_populates="user", cascade="all, delete-orphan"
    )
    

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(Integer, primary_key=True, index=True)
    subscription_name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    validity = Column(Integer, nullable=False)  # Validity in days
    data_limit = Column(Float, nullable=False)  # Data limit in GB

    # Relationship with ActiveSubscription
    active_subscriptions = relationship(
        "ActiveSubscription", 
        back_populates="subscription", 
        cascade="all, delete-orphan"
    )


class ActiveSubscription(Base):
    __tablename__ = "active_subscription"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.subscription_id", ondelete="CASCADE"), nullable=False)
    subscription_name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(255), nullable=True)
    validity = Column(Integer, nullable=False)  # Validity in days
    data_limit = Column(Float, nullable=False)  # Data limit in GB
    purchase_date = Column(DateTime, nullable=True)  # Nullable for free plans
    validity_end_date = Column(DateTime)
    # Relationships
    user = relationship("User", back_populates="active_subscription")
    subscription = relationship("Subscription", back_populates="active_subscriptions")

def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Calculate and set the validity_end_date based on purchase_date and validity
        self.validity_end_date = self.purchase_date + timedelta(days=self.validity) 

class FileUploadLog(Base):
    __tablename__ = "file_upload_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    table_name = Column(String(255), nullable=False)
    uploaded_at = Column(DateTime, default=func.now())


class MasterTable(Base):
    __tablename__ = 'master_table'

    master_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    email_id = Column(String(255), unique=True, nullable=True)
    phone_number = Column(String(15), unique=True, nullable=True)
    current_location = Column(String(255), nullable=True)
    total_experience = Column(String(50),nullable=True)


class DataTable(Base):
    __tablename__ = "data_table"
    
    id = Column(Integer, ForeignKey('master_table.master_id'), primary_key=True)
    # No predefined columns for dynamic schema; additional columns will be added dynamically

#data history table
class DataHistory(Base):
    __tablename__ = "data_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.subscription_id", ondelete="CASCADE"), nullable=False)
    total_records = Column(Integer, nullable=False, default=0)
    downloaded_records = Column(Integer, nullable=False, default=0)
    remaining_records = Column(Integer, nullable=False, default=0)

    # Relationships
    user = relationship("User", back_populates="data_histories")


class EmailBroadcasting(Base):
    __tablename__ = 'email_broadcasting'

    email_broadcasting_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=False)
    email_id = Column(String(255), nullable=False)
    app_password = Column(String(255), nullable=False)

    # Optional: Relationship with the `users` table
    user = relationship('User', back_populates='email_broadcasting')

Base.metadata.create_all(bind=engine)