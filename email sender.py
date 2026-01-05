import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = "koopatroopa725@gmail.com"
EMAIL_PASSWORD = "nuvq letk ujzf ypgk"

TO_EMAIL = "gt2oyh7jy0@jxpomup.com"

msg = MIMEMultipart()
msg["From"] = EMAIL_ADDRESS
msg["To"] = TO_EMAIL
msg["Subject"] = "i hate noggers"

body = "'sup my knee-grow"
msg.attach(MIMEText(body, "plain"))


try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
