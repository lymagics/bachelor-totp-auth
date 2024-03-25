from io import BytesIO

from django.contrib.auth import authenticate

import pyqrcode

from auth.errors import InvalidCredentials
from users.models import User


def login(username: str, password: str, token: str) -> User:
    user = authenticate(username=username, password=password)
    if user is None or not user.verify_totp(token):
        error = 'Invalid username, password or token.'
        raise InvalidCredentials(error)
    return user


def qrcode_create(user: User) -> BytesIO:
    url = pyqrcode.create(user.totp_uri)
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream
