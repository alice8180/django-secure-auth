from django.db.models.signals import post_save
from django.dispatch import receiver

# import models hare
from accounts.models import CustomUser
from accounts.models import Profile

# custom class or functions
from accounts.helper import generate_one_time_url

# send email function
from notifications.services import send_verification_mail 

# import exception
from rest_framework.exceptions import ValidationError as DRFValidationError

# import logger 
from utils.logger import accounts_log_debug, accounts_log_info, accounts_log_warning, accounts_log_error




# create your signals hare 


"""email verification signal"""
@receiver(post_save, sender=CustomUser)
def send_verification_email_signal(sender, instance, created, **kwargs):
    try:
        if created and not instance.is_verified:

            # create blank profile
            Profile.objects.create(user=instance)
            url = generate_one_time_url(user=instance)
            
            # send verification mail for verify email id
            send_verification_mail(user=instance, subject="Verify your account" ,url=url, template="emails/set_new_password.html")
            accounts_log_info(message="Send verification email successfully from Signals", user=instance)
            
    except DRFValidationError as e:
        accounts_log_error(message=f"verify email not send | {e} ", user=instance)
        raise DRFValidationError(e)
    except Exception as e:
        raise Exception(e)