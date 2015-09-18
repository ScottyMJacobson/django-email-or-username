from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts import backends


class TestLogin(TestCase):
    def setUp(self):
        self.username = "test_user0"
        self.email = "test0@email.com"
        self.password = "test_password0"
        self.user =  get_user_model().objects.create_user(
                username = self.username,
                email = self.email,
                password = self.password,
            )
        self.username2 = "test_user1"
        self.email2 = "test1@email.com"
        self.password2 = "test_password1"
        self.user2 =  get_user_model().objects.create_user(
                username = self.username2,
                email = self.email2,
                password = self.password2,
            )

    def test_username_login(self):
        login_result = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login_result)

    def test_email_login(self):
        login_result = self.client.login(username=self.email, password=self.password)
        self.assertTrue(login_result)

    def test_username_fail(self):
        login_result = self.client.login(username="", password=self.password)
        self.assertFalse(login_result)

    def test_different_password_fail(self):
        login_result = self.client.login(username=self.email2, password=self.password)
        self.assertFalse(login_result)

    def test_password_fail(self):
        login_result = self.client.login(username=self.username, password="")
        self.assertFalse(login_result)


class TestBackend(TestCase):
    def setUp(self):
        self.username = "test_user"
        self.email = "test@email.com"
        self.password = "test_password"
        self.user =  get_user_model().objects.create_user(
                username = self.username,
                email = self.email,
                password = self.password,
            )
        self.dummy_backend = backends.EmailOrUsernameAuthBackend()

    def test_lookup_by_username(self):
        result_user = self.dummy_backend._lookup_user(self.username)
        self.assertEqual(result_user.id, self.user.id)

    def test_fail_lookup_by_username(self):
        result_user = self.dummy_backend._lookup_user("")
        self.assertEqual(result_user, None)

    def test_fail_lookup_by_partial_username(self):
        result_user = self.dummy_backend._lookup_user(self.username[0:-1])
        self.assertEqual(result_user, None)

    def test_lookup_by_email(self):
        result_user = self.dummy_backend._lookup_user(self.email)
        self.assertEqual(result_user.id, self.user.id)
        
    def test_authenticate_by_username(self):
        result_user = self.dummy_backend.authenticate(self.username, self.password)
        self.assertEqual(result_user.id, self.user.id)

    def test_authenticate_by_email(self):
        result_user = self.dummy_backend.authenticate(self.email, self.password)
        self.assertEqual(result_user.id, self.user.id)

    def test_get_user(self):
        result_user = self.dummy_backend.get_user(self.user.id)
        self.assertEqual(result_user.id, self.user.id)

    def test_fail_get_user(self):
        result_user = self.dummy_backend.get_user(-1)
        self.assertEqual(result_user, None)

    def test_case_insensitive_email(self):
        result_user = self.dummy_backend._lookup_user(self.email.upper())
        self.assertEqual(result_user.id, self.user.id)

    def test_case_insensitive_username(self):
        result_user = self.dummy_backend._lookup_user(self.username.upper())
        self.assertEqual(result_user.id, self.user.id)

