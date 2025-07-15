import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Replace with your Gmail and App Password
EMAIL_ADDRESS = "dambaliuday@gmail.com"
EMAIL_PASSWORD = "fzco reev gwsn shpr"  # Use Gmail App Password (not your normal password)

# Recipient Email
to_email = "udaidambali281104@example.com"

# Email Content
subject = "Test Email from Python"
body = "This is a test email sent from Python using SMTP."

# Create the email message
msg = MIMEMultipart()
msg['From'] = EMAIL_ADDRESS
msg['To'] = to_email
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

# Send the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print("✅ Email sent successfully!")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
