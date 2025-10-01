from django.test import TestCase

# import models hare 
from accounts.models import CustomUser



# create your test logic hare


class CustomUserModelTest(TestCase):

    def test_create_user_with_valid_data(self):
        user = CustomUser.objects.create_user(
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            password="strongpassword123"
        )
        self.assertEqual(user.email, "test@mail.com")
        self.assertTrue(user.check_password("strongpassword123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            email="admin@mail.com",
            first_name="Admin",
            last_name="User",
            password="adminpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_email_is_required(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="",
                first_name="No",
                last_name="Email",
                password="nopass"
            )

    def test_user_string_representation(self):
        user = CustomUser.objects.create_user(
            email="string@mail.com",
            first_name="String",
            last_name="Test",
            password="stringpass"
        )
        self.assertEqual(str(user), "String-Test")  # ধরে নিচ্ছি __str__ email return করে



from django.test import TestCase
from accounts.serializers import CreateAccountSerializer
from accounts.models import CustomUser


class CreateAccountSerializerTest(TestCase):

    def test_valid_serializer_creates_user(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "password": "password123"
        }
        serializer = CreateAccountSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertFalse(user.is_verified)  # read_only field default এ False

    def test_password_is_write_only(self):
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "password": "password123"
        }
        serializer = CreateAccountSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        serializer.save()
        serialized_data = serializer.data

        self.assertNotIn("password", serialized_data)  # password expose হয় না
        self.assertIn("email", serialized_data)
        self.assertIn("first_name", serialized_data)


