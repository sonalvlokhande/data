# app/main.py
from fastapi import FastAPI
from common_api.routes import common_router
from admin_api.routes import admin_router
from user_api.routes import user_router
from admin_api.manage_users import manageuser_router
from admin_api.file_upload import file_upload_router 
from admin_api.zip_file import zip_file_router
from common_api.My_profile import myprofile_router
from admin_api.subscription import subscription_router  
from testfile import test_router
from admin_api.fileuploadcsv import fileuploadcsv_router 
from user_api.download_rec import download_router
from emaildata.useremail_config import email_router
from emaildata.bulk_mail import bulk_mail_router

app = FastAPI()

# Include routers
app.include_router(common_router, prefix="/common", tags=["common"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(manageuser_router, prefix="/admin/manageuser",tags=["admin","manageuser"])
app.include_router(file_upload_router, prefix="/admin/fileupload", tags=["admin", "fileupload"])
app.include_router(zip_file_router, prefix="/admin/zipupload", tags=["admin", "zipupload"])
app.include_router(myprofile_router, prefix="/common/myprofile", tags=["common", "myprofile"])
app.include_router(subscription_router, prefix="/admin/subscription", tags=["admin", "subscription"])
app.include_router(file_upload_router, prefix="/file", tags=["File Upload"])
app.include_router(fileuploadcsv_router, prefix="/admin/fileuploadcsv", tags=["admin", "fileuploadcsv"])    
app.include_router(test_router, prefix="/test", tags=["test"])
app.include_router(download_router, prefix="/download", tags=["download"])
app.include_router(email_router, prefix="/email_config", tags=["Email Configuration"])
app.include_router(bulk_mail_router, prefix="/bulk_mail", tags=["Bulk Mail"])