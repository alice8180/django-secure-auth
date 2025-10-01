from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

# import models hare
from accounts.models import CustomUser



# create your testes 


class TestValidUser(TestCase):
    

    
    def dummy_user(self):
        dummy_user = {
            "first_name": "Alice",
            "last_name": "Wick",
            "email": "alice.web.1011@gmail.com",
            "password": "alice"
        }
        return dummy_user
    
    
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            **self.dummy_user()
        )
        
        self.assertEqual(first=user.first_name, second="Alice", msg="miss mass user.first_name or provide first_name" )
        self.assertEqual(first=user.last_name, second="Wick", msg="miss mass user.last_name or provide last_name" )
        self.assertEqual(first=user.email, second="alice.web.1011@gmail.com", msg="user email or provide email miss mass" )
        self.assertTrue(expr=user.check_password("alice"), msg="user.password or provide passwd not mass!!")
        self.assertTrue(expr=user.is_active, msg="user not active")
        print("----------> create user check successfully!! <------------")
        
    
    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(**self.dummy_user())

        self.assertTrue(expr=user.is_staff, msg="admin user allows is_staff")
        self.assertTrue(expr=user.is_superuser, msg="admin user allows is_superuser=true")

        print("---------> create superuser check successfully <-------------")
        
        
        


from accounts.serializers import CreateAccountSerializer
class TestCreateSerializer(TestCase):

    def dummy_user(self):
        dummy_user = {
            "first_name": "Alice",
            "last_name": "Wick",
            "email": "alice.web.1011@gmail.com",
            "password": "alice"
        }
        return dummy_user
    
    def test_valid_serializer_data(self):
        serializer = CreateAccountSerializer(data=self.dummy_user())
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        user = serializer.save()
        self.assertIsInstance(obj=user, cls=CustomUser, msg="CreateAccountSerializer create obj other class")
        self.assertEqual(first=user.email, second="alice.web.1011@gmail.com", msg="provide email or serializer validate email not mass")
        self.assertEqual(first=user.first_name, second="Alice", msg="miss mass serializer first_name or provide first_name" )
        self.assertEqual(first=user.last_name, second="Wick", msg="miss mass serializer last_name or provide last_name" )
        self.assertTrue(expr=user.check_password("alice"), msg="provide password or serializer password not mass")
        print("-------------> CreateAccountSerializer check successfully <--------------")
        


# Amra akhon unit test korsi, akhon porjonto ami atake halka vabe niyesilm, kintu akhon bujte parisi ata tota powerful
from accounts.models import EmailVerificationToken
class TestVerifyEmail(TestCase):
    """
    EmailVerificationToken model test cases
    """

    def setUp(self):
        USER = {
            "first_name": "Alice",
            "last_name": "Wick",
            "email": "alice.web.1011@gmail.com",
            "password": "alice"
        }
        self.user = CustomUser.objects.create_user(**USER)

    def test_verify_email_model(self):
        token = EmailVerificationToken.objects.create(user=self.user, token="abcde12345")
        self.assertIsNotNone(token.expired_at)

        expected_expire = timezone.now() + timedelta(minutes=30)
        delta = abs((token.expired_at - expected_expire).seconds)
        self.assertTrue(delta < 5)

    def test_custom_expire(self):
        custom_expire = timezone.now() + timedelta(hours=1)
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token="xyz789",
            expired_at=custom_expire
        )
        self.assertEqual(token.expired_at, custom_expire)

    def test_token_validate(self):
        token = EmailVerificationToken.objects.create(user=self.user, token="abcd1234")
        self.assertTrue(token.is_valid())

    def test_invalid_used_token(self):
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token="ABCD1234",
            is_used=True
        )
        self.assertFalse(token.is_valid())

    def test_expired_token(self):
        expired_time = timezone.now() - timedelta(minutes=1)
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token="abcd1234",
            expired_at=expired_time
        )
        self.assertFalse(token.is_valid())
    

    
# accounts/tests/test_email_token.py
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser, EmailVerificationToken

class EmailVerificationTokenTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="StrongPass123"
        )

    def test_auto_expiry_set_on_save(self):
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token="abc123"
        )
        self.assertIsNotNone(token.expired_at)
        expected_expiry = timezone.now() + timedelta(minutes=30)
        # check almost equal (few seconds difference allowed)
        self.assertTrue(abs((token.expired_at - expected_expiry).seconds) < 5)

    def test_custom_expiry_respected(self):
        custom_expiry = timezone.now() + timedelta(hours=1)
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token="xyz456",
            expired_at=custom_expiry
        )
        self.assertEqual(token.expired_at, custom_expiry)

    def test_token_is_valid_initially(self):
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token="validtoken"
        )
        self.assertTrue(token.is_valid())

    def test_token_invalid_if_used(self):
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token="usedtoken",
            is_used=True
        )
        self.assertFalse(token.is_valid())

    def test_token_invalid_if_expired(self):
        expired_time = timezone.now() - timedelta(minutes=1)
        token = EmailVerificationToken.objects.create(
            user=self.user,
            token="expiredtoken",
            expired_at=expired_time
        )
        self.assertFalse(token.is_valid())



