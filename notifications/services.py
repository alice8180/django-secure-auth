from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpRequest
from django.conf import settings
from django.utils.timezone import now
# import typing
from typing import Optional

# errors classes
from django.core.mail import BadHeaderError
from rest_framework.exceptions import ValidationError as DRFValidationError

# celery task
from celery import shared_task

# import logger
from utils.logger import utils_log_debug, utils_log_info, utils_log_warning, utils_log_error




# create mail functions and classes

def send_verification_mail(user:object, subject:str, url:int, template:str, request:Optional[HttpRequest]=None) -> None:
    try:
        from_email = settings.EMAIL_HOST_USER
        to_email = [user.email]

        html_content = render_to_string(template, {
            "user": user,
            "otp": url,
            "current_year": now().year,
        })

        email = EmailMultiAlternatives(subject, "", from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
        utils_log_info(message= f"send verification email successfully!! to : {user.email}", user=user)
        
    except BadHeaderError as e:
        utils_log_warning(message="invalid email or google service problems", request=request, user=user)
        raise DRFValidationError({"email": "invalid email or other service error"})

    
    except Exception as e:
        utils_log_error(message=f"error in send_verification_mail() function!! | errors: {str(e)}", request=request, user=user)
        raise Exception(f"Problem on send_verification_mail | {str(e)}")
        