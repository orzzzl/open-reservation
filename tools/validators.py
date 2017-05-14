import re


def validate(pattern, content):
    return content and pattern.match(content)


def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,25}$")
    return validate(USER_RE, username)


def valid_password(password):
    PASS_RE = re.compile(r"^.{3,25}$")
    return validate(PASS_RE, password)


def valid_email(email):
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    return validate(EMAIL_RE, email)
