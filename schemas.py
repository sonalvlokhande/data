from pydantic import BaseModel
from typing import Optional
from typing import List, Dict,Optional
from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    mobile: str
    profession: str
    city: str
    subscription_name: Optional[str]

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    # Add other fields as needed

#schema for user signup request
class UserSignupSchema(BaseModel):
    username: str
    email: str
    mobile: str
    profession: str
    city:str
    subscription_name: Optional[str] = "free"

class ActiveSubscriptionData(BaseModel):
    id: int
    user_id: int
    subscription_id: int
    subscription_name: str
    username: str
    email: str
    mobile: str
    profession: Optional[str] = None  # Mark as Optional
    city: Optional[str] = None
    purchase_date: Optional[datetime] = None  # Can be null for free subscription
    validity_end_date: Optional[datetime] = None

# Success Response Schema for Signup
class SignupResponse(BaseModel):
    message: str
    data: ActiveSubscriptionData

'''class UserSubscription(BaseModel):
    id: int
    username: str
    email: str
    mobile: str
    profession: str
    city: str
    role: str
    subscription_name: str '''


class OTPRequest(BaseModel):
    mobile: str

class OTPResponse(BaseModel):
    msg: str
    mobile: str
    otp: int 

class OTPVerify(BaseModel):
    mobile: str
    otp: str       

class AdminUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    profession: Optional[str]
    city: Optional[str]
    subscription_name: Optional[str]

class SubscriptionUpdate(BaseModel):
    subscription_name: str  # e.g., "free", "premium", "basic", etc.

class ManageUserResponse(BaseModel):
    id: int
    username: str
    email: str
    mobile: str
    profession: str
    city :str
    role: str
    subscription_name: Optional[str]

class MyprofileUserResponse(BaseModel):
    id: int
    username: str
    email: str
    mobile: str
    profession: str
    city :str
    role: str
    subscription_name: Optional[str]

class MyprofileAdminResponse(BaseModel):
    id: int
    username: str
    email: str
    mobile: str
    profession: str
    city: str
    role: str
    subscription_name: str
    
class UserIDRequest(BaseModel):
    id: int 

class DeleteUserRequest(BaseModel):
    id: int

class SubscriptionUpdate(BaseModel):
    id: int  # User ID
    subscription_name: str


class Config:
    from_attributes = True
        
class UploadFileResponse(BaseModel):
    message: str
    table_name: str

class UploadZipResponse(BaseModel):
    message: str
    tables: List[Dict[str, str]]

class ErrorResponse(BaseModel):
    detail: str

class UserUpdate(BaseModel):
    id: int # Include the user ID
    email: Optional[str]
    mobile: Optional[str]
    profession: Optional[str]
    city: Optional[str]
    #subscription_name: Optional[str]

class UserSubscription(BaseModel):
    id: int
    username: str
    email: str
    mobile: str
    profession: Optional[str]
    city: Optional[str]
    role: str
    subscription: ActiveSubscriptionData  # Include subscription details in the response

#subscription
class SubscriptionIDRequest(BaseModel):
    subscription_id: int

class SubscriptionBase(BaseModel):
    subscription_name: str
    price: float
    description: Optional[str] = None
    validity: int
    data_limit: float

class SubscriptionCreate(SubscriptionBase):
    subscription_name: str
    price: float
    description: Optional[str] = None
    validity: int
    data_limit: float
    
class SubscriptionUpdate(BaseModel):
    subscription_id: int
    subscription_name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    validity: Optional[int] = None
    data_limit: Optional[float] = None

class SubscriptionResponse(SubscriptionBase):
    subscription_id: int
    
#  master table schema 
class MasterTableSchema(BaseModel):
    
    name: str
    email_id: str
    phone_number: str
    curret_location: str
    total_experience: str

# Output schema
class SubscriptionDetails(BaseModel):
    subscription_id: int
    subscription_name: str
    description: str
    validity: int
    data_limit: float
    price: float

class UserSubscriptionResponse(BaseModel):
    user_id: int
    username: str
    email: str
    mobile: str
    profession: str
    subscription: SubscriptionDetails

class SubscriptionPurchaseSchema(BaseModel):
    subscription_id: int  # ID of the subscription being purchased
    mobile: Optional[str] = None  # Mobile number of the user (optional)
    user_id: Optional[int] = None  # User ID (optional)

#user info  
class SubscriptionResponse(BaseModel):
    subscription_id: int
    subscription_name: str
    price: float
    validity: int
    data_limit: float
    description: Optional[str] = None
    purchase_date: Optional[datetime]  # Include purchase_date
    validity_end_date: Optional[datetime]  # Include validity_end_date

class DownloadHistoryResponse(BaseModel):
    total_records: int
    downloaded_records: int
    remaining_records: int

class UserInfoResponse(BaseModel):
    id: int
    username: str
    email: str
    mobile: str
    profession: Optional[str]
    city: Optional[str]
    subscription :SubscriptionResponse
    download_history: Optional[DownloadHistoryResponse] = None


# download_records
class DownloadRequest(BaseModel):
    id: int
    table_name: str
    no_of_records: int

class BulkMailRequest(BaseModel):
    id: int
    table_name: str
    subject: str
    body: str

class EmailBroadcastingCreate(BaseModel):
    id: int
    email_id: str
    app_password: str

class Config:
        from_attributes = True