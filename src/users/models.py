from hashlib import md5

from django.contrib.auth.models import AbstractUser
from django.db import models

import pyotp


class User(AbstractUser):
    """
    User entity.
    """
    email = models.EmailField(unique=True)
    otp_secret = models.CharField(max_length=32)

    @property
    def avatar_url(self) -> str:
        avatar_hash = md5(self.email.encode()).hexdigest()
        return f'https://www.gravatar.com/avatar/{avatar_hash}?d=mp'
    
    @property
    def totp_uri(self):
        return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=2FA-Demo' \
            .format(self.username, self.otp_secret)

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token, valid_window=2)
