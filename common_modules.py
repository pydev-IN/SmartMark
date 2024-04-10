"""
Contains all Python modules using in the application
"""
import datetime
from jose import jwt
from json_struct import StudentMaster, StaffMaster
from passlib.context import CryptContext

HASH_ALGO = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 45
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "561ed10213d979343c8c9aa6d34064be20b453c005a026feae1b2b02cac28114"
SMTP_SECRET = "wnoh iwnv suvp snyf"
SMTP_SENDER = "rashmithdevadiga@gmail.com"
# Authentication and Authorization


def verify_password(plain_pwd, hashed_pwd):
    """
    verifies hash value of the given password
    :param plain_pwd:  user password in string value
    :param hashed_pwd: hash value of a string/password
    :return:
    """
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_password_hash(pwd):
    """
    converts string/password into hash value
    :param pwd: password in plain string
    :return: hash value
    """
    return pwd_context.hash(pwd)


def authenticate_user(username: str, password: str, user_role: str):
    """
    This will authenticate if user is valid or not
    :param username: username of user
    :param password: password of user
    :param user_role: Role of user ["Admin", "Staff", "Student"]
    :return: userdata
    """
    from DB_Ops import select_user
    status, user = select_user(username, user_role)
    if not status:
        return False
    if not verify_password(password, user.password.get_secret_value()):
        return False
    return user


def create_access_token(data: dict, expires_delta: datetime.timedelta or None = None):
    """
    generates access token for a user
    :param data: userdata
    :param expires_delta: expiration time delta
    :return: newly created access token for the user data
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGO)

    return encode_jwt


def send_email(recipient, subject, body):
    import smtplib

    FROM = SMTP_SENDER
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, SMTP_SECRET)
        server.sendmail(FROM, TO, message)
        server.close()
        return True
    except:
        return False


def invite_user_mail(name: str, username: str, email: str, password: str):
    """
    This will send an email notification to newly created users.
    :param name: name of the user.
    :param username: username of the user.
    :param email: email address of the user.
    :param password: password of the user.
    :return: bool= status of email.
    """
    mail_body = f"""Hello {name}\n\n
This is to inform you that your account is created. Requesting you to use below username and password for login.\n
username: {username}\npassword: {password}\n
this email is intended to {email} please do not reply on this mail as this is auto generated\n
Thank you.."""
    return True
    # return send_email(email, "SmartMark Notification", mail_body)

