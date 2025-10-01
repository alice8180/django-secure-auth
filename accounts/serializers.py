from django.http import Http404
from django.core.validators import EmailValidator

# import rest_framework hare
from rest_framework import serializers
from rest_framework.authentication import authenticate
from rest_framework.generics import get_object_or_404

# import exceptions hare
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

# import models hare
from accounts.models import CustomUser
from accounts.models import Profile


# create your serializers hare

    
class DummySerializer(serializers.Serializer):
    pass


class CreateAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password","is_verified"]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields =  ["is_verified"]
        
        
    def create(self, validated_data):
        # Manager এর create_user() ব্যবহার হবে
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user
    




# reset password used this serializer
# resend verify email used this serializer 
class ValidateEmailSerializer(serializers.Serializer):
    """
    Used for: reset-password, resend-verify-email, etc.
    - Accepts email, normalizes it, finds user (case-insensitive).
    - Returns attrs with `user`.
    """
    email = serializers.EmailField(min_length=2, max_length=155)

    def validate_email(self, value: str) -> str:
        
        # normalize input
        return value.strip().lower()

        
        
    def validate(self, attrs):
        email = attrs.get("email")
        user = CustomUser.objects.filter(email__exact=email).first()
        if not user:
            raise serializers.ValidationError({"email": "No account found with this email."})
        attrs["user"] = user
        return attrs



class LoginUserSerializer(serializers.Serializer):
    """
    Simple login serializer — email normalized here as well.
    """
    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(min_length=8, max_length=128)

    def validate_email(self, value: str) -> str:
        # normalize input once here
        return value.strip().lower()



class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8 ,max_length=15)
    
    
    
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "is_verified"]

# profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ["user", "gender", "phone", "address", "profile_picture", ]
        
    def validate_gender(self, value:str) -> str:
        value = value.capitalize() # jodi extra space thake seta remove korbe
        return value # user akhon jodi "male" likhe tahole seta ke "Male" kora hobe, 