import smtplib

from features import app, mail
from flask_mail import Mail, Message


def send_email_smtp(sender, receiver, domain, server_user, server_user_password, server_port):
    message = f"""\
    Subject: Hi Mailtrap
    To: {receiver}
    From: {sender}

    This is a test e-mail message."""

    with smtplib.SMTP(domain, server_port) as server:
        server.login(server_user, server_user_password)
        server.sendmail(sender, receiver, message)


def send_email_flask(sender, receiver):
    with app.app_context():
        smail = Mail(app)
        message = f"""\
            Subject: Hi Mailtrap
            To: {receiver}
            From: {sender}

            This is a test e-mail message."""

        msg = Message('Hello', sender=sender, recipients=[receiver])
        msg.body = message
        smail.send(msg)
