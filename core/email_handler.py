# core/email_handler.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# You'll need to create an App Password from your Google account
EMAIL_ADDRESS = "cricklightprime@gmail.com"
EMAIL_PASSWORD = "fzco reev gwsn shpr"  # NOT your main password

def send_email(to_email, subject, body):
    try:
            # Email setup
            message = MIMEMultipart()
            message["From"] = EMAIL_ADDRESS
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Send email
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
            server.quit()

            return True, "✅ Email sent successfully!"

    except Exception as e:
        return False, f"❌ Failed to send email: {e}"   