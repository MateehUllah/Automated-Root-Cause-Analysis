import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_RECEIVERS = os.getenv("EMAIL_RECEIVER").split(",")

def send_email_alert(subject, message):
    """
    Sends an email alert to multiple recipients using SMTP.
    
    Args:
        subject (str): Email subject line
        message (str): Email body content
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_USERNAME
        msg["To"] = ", ".join(EMAIL_RECEIVERS)  
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() 
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        server.sendmail(SMTP_USERNAME, EMAIL_RECEIVERS, msg.as_string())

        server.quit()
        print("✅ Email Sent Successfully to Multiple Recipients!")

    except Exception as e:
        print(f"❌ Error sending email: {e}")