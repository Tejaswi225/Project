
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(username):
    # Email configuration
    s_email = ''  # Change this to your email address
    r_email = ''  # Change this to the recipient's email address
    password = ''  # Change this to your email password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Login Notification"
    message["From"] = r_email
    message["To"] = s_email

    # Email content
    text = f"User {username} logged in successfully."
    html = f"<p>User {username} logged in successfully.</p>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(r_email, password)
        server.sendmail(r_email, s_email, message.as_string())

def send(msg,mail):
    # Email configuration
    r_email = 'bomma.chiru@gmail.com'  # Change this to your email address
    s_email = mail  # Change this to the recipient's email address
    password = 'cxds xnfo vkha qmlo'  # Change this to your email password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Login Notification"
    message["From"] = r_email
    message["To"] = s_email

    # Email content
    html = f"""
            <h2>Hello User,</h2>
            <h5>{msg}</h5>
                """

    part2 = MIMEText(html, "html")

    message.attach(part2)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(r_email, password)
        server.sendmail(r_email, s_email, message.as_string())


send("chiru",['bommachiranjeevi13@gmail.com','20jr1a0539@gmail.com'])