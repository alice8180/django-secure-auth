from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid

# import model manager 
from accounts.manager import UserManager



# Create your models here.


class BaseModel(models.Model):
    
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=155, unique=True)
    
    is_verified = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    
    def __str__(self):
        return f"{self.first_name}-{self.last_name}"
    



class Profile(BaseModel):
    GENDER = [
        ("M", "Male"),
        ("F", "Female")
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(choices=GENDER, max_length=7, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    address = models.TextField(max_length=1000, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email}"
    
    

    
class EmailVerificationToken(BaseModel):
    # uuid, created_at, updated_at include
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expired_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # if not self.uuid : karon jodi kono new object ashe tokhon tar kono uuid thakena , tai check kora hosse
        # if not self.expired_at : karon jodi ami kono jaigate custom cave ....object.create(expired_at=30mn) kori , tokhon ai save method ta amader custom date time tai rakhbe
        if not self.uuid and not self.expired_at:
            self.expired_at = timezone.now() + timedelta(minutes=30)  # 30 min valid

        super().save(*args, **kwargs)
                     
                     
    def is_valid(self):
        return not self.is_used and self.expired_at > timezone.now()
    
    
    

    
    
    