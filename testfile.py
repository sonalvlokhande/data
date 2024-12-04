########### Script to send bulk mail to uploaded file's email ids ###########
import smtplib
from fastapi import FastAPI,APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, Session
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

# Database Setup
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:MahitNahi%4012@localhost/larg_data"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"  # Use your SMTP server
SMTP_PORT = 587
SENDER_EMAIL = "jamal.heena68@gmail.com"
SENDER_PASSWORD = "dhvl lrsc kaij ufgs"


# FastAPI instance
test_router = APIRouter()

# Pydantic Model for email content
class EmailContent(BaseModel):
    subject: str
    body: str
    table_name: str  # Add the table_name field to the schema

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to send emails
def send_bulk_email(subject: str, body: str, recipient_list: List[str]):
    try:
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Establish a connection to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            # Send email to all recipients
            message['To'] = recipient_list[0]  # Set the first recipient in the To header
            server.sendmail(SENDER_EMAIL, recipient_list, message.as_string())  # Send to all recipients in the list

        return "Emails sent successfully!"
    except Exception as e:
        return f"Failed to send emails: {str(e)}"


# Bulk mail API endpoint
@test_router.post("/send_bulk_mail")
async def send_bulk_mail(content: EmailContent, db: Session = Depends(get_db)):
    # Reflect the table dynamically from the provided table_name using MetaData.reflect()
    try:
        metadata.reflect(bind=engine)  # Reflect all tables in the database
        if content.table_name not in metadata.tables:
            raise HTTPException(status_code=400, detail=f"Table {content.table_name} not found in the database.")
        
        # Fetch the table dynamically
        table = metadata.tables[content.table_name]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reflecting table {content.table_name}: {str(e)}")

    # Query the email IDs from the specified table
    try:
        emails = db.query(table.c.email_id).all()  # Assuming email_id is the column containing emails
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying table {content.table_name}: {str(e)}")

    if not emails:
        raise HTTPException(status_code=404, detail=f"No email IDs found in the {content.table_name} table.")
    
    # Extract email list
    email_list = [email[0] for email in emails]  # Emails will be a list of tuples, so extract the email_id

    # Send bulk email
    result = send_bulk_email(content.subject, content.body, email_list)
    return {"message": result}












"""import smtplib

def test_smtp_connection():
    try:
        smtp_host = "smtp.gmail.com"
        smtp_port = 587

        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.ehlo()  # Greet the server
            smtp.starttls()  # Initiate STARTTLS
            smtp.login("jamal.heena68@gmail.com", "zhjq eehr qivj wehr")  # Test login
            print("STARTTLS connection established successfully.")
    except Exception as e:
        print(f"Failed to establish connection: {e}")

test_smtp_connection()"""