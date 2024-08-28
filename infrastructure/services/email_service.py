from email.message import EmailMessage
import ssl
import smtplib

def send_confirmation_email(recipient_email, token):
    email_sender = ""
    password = ""
    subject = "Confirma tu registro en TaskMaster"
    body = f"""
    Hola,

    Por favor confirma tu registro haciendo clic en el siguiente enlace:
    http://yourdomain.com/confirm/{token}

    Saludos,
    TaskMaster Team
    """
##Aqui tenemos que cambiarle el dominio
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = recipient_email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, password)
        smtp.sendmail(email_sender, recipient_email, em.as_string())
