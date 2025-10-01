from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now, timedelta

# import models hare
from accounts.models import CustomUser
from accounts.models import EmailVerificationToken

# import helper function and classes
from celery_tasks.helper import ManageInvalidObjects

# errors classes
from django.core.mail import BadHeaderError
from rest_framework.exceptions import ValidationError as DRFValidationError

# celery task
from celery import shared_task

# import logger
from utils.logger import utils_log_debug, utils_log_info, utils_log_warning, utils_log_error




# create task hare


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_celery_mail(self, email:str, subject:str, template:str, context:dict) -> None:
    try:
        print("check 3")
        from_email = settings.EMAIL_HOST_USER
        print("check 4")
        to_email = [email]

        html_content = render_to_string(template_name=template, context=context)

        email = EmailMultiAlternatives(subject, "", from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
        utils_log_info(message= f"send verification email successfully!! to : {email}")
    
    
    except BadHeaderError as e:
        utils_log_warning(message="invalid email or google service problems")
        raise
    
    except Exception as e:
        utils_log_error(message=f"error in send_verification_mail() function!! | errors: {str(e)}")
        raise
        
        



# auto clean unverified users 
@shared_task
def cleanup_unverified_users():
    threshold = now() - timedelta(hours=24)
    manage_ooj = ManageInvalidObjects(model=CustomUser)
    manage_ooj.filter_objects(is_verified=False, created_at__lt=threshold)
    count_users = manage_ooj.clean_obj()
    
    utils_log_info(message=f"unverified or inactive {count_users} users cleaned successfully!!")


# auto clean invalid verify token
@shared_task
def cleanup_invalid_verify_token():
    threshold = now() - timedelta(hours=24) 
    manage_ooj = ManageInvalidObjects(model=EmailVerificationToken)
    manage_ooj.filter_objects(created_at__lt = threshold) # akhene tohh 10s agge jodi kono obj create hoy seta filter hobe, kintu jodi 11s agge create hoy tahole ki hobe?? 
    count_token = manage_ooj.clean_obj()
    
    utils_log_info(message=f"invalid verify urls : {count_token} delete successfully!!")
    
