from io import BytesIO

from django.test import TestCase

from auth import services
from auth.errors import InvalidCredentials
from users.tests.factories import UserFactory

import pyotp
import pyqrcode


class TestServices(TestCase):
    """
    Test case for auth services.
    """
    def test_login(self):
        # given
        new_user = UserFactory()
        totp = pyotp.TOTP(new_user.otp_secret)
        # when
        user = services.login(username=new_user.username,
                              password='testpass123',
                              token=totp.now(),)
        # then
        self.assertIsNotNone(user)
        self.assertEqual(user, new_user)

    def test_login_fail_user_does_not_exist(self):
        # then
        with self.assertRaises(InvalidCredentials):
            services.login(username='bob',
                           password='testpass123',
                           token='123456',)

    def test_login_fail_wrong_password(self):
        # given
        user = UserFactory()
        # then
        with self.assertRaises(InvalidCredentials):
            services.login(username=user.username,
                           password='wrongpassword',
                           token='123456',)
            
    def test_login_fail_worng_token(self):
        # given 
        user = UserFactory()
        # then
        with self.assertRaises(InvalidCredentials):
            services.login(username=user.username,
                           password='testpass123',
                           token='123456',)
            
    def test_qrcode_create(self):
        # given
        user = UserFactory()
        url = pyqrcode.create(user.totp_uri)
        stream = BytesIO()
        url.svg(stream, scale=3)
        # when
        qrcode = services.qrcode_create(user)
        # then
        self.assertIsInstance(qrcode, BytesIO)
        self.assertEqual(qrcode.getvalue(), stream.getvalue())
