from django.contrib import admin

# import models hare
from accounts.models import CustomUser, Profile, EmailVerificationToken

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "is_active", "is_staff", "is_superuser", "is_verified")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "is_superuser")
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["get_user_first_name", "gender", "phone",]
    
    def get_user_first_name(self, obj):
        return obj.user.first_name
    get_user_first_name.short_description = "First Name"
    
@admin.register(EmailVerificationToken)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ["get_user_first_name", "is_used"]
    
    def get_user_first_name(self, obj):
        return obj.user.first_name
    get_user_first_name.short_description = "First Name"
    