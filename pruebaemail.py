import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

load_dotenv()

email_sender = "taskmasterspport@gmail.com"
password = "rzjt yaky xlxg vtvw"
email_reciver = "piopenagos8@gmail.com"

subject = "Bienvenido a TaskMaster"
body = """
    Aqui agregamos el mensaje
"""

em = EmailMessage()
em["From"] = email_sender
em["To"] = email_reciver
em["Subject"] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465,context= context) as smtp:
    smtp.login(email_sender, password)
    smtp.sendmail(email_sender, email_reciver, em.as_string())