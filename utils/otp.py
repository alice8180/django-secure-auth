from django.utils import timezone
from random import randint


# create your function hare


def generate_otp():
    return randint(100000,999999)


# for email verification
def validate_otp(user, otp_input):
    otp_obj = user.verify_email.first()
    if not otp_obj or otp_obj.is_expired() or otp_obj.attempt_count >= 3:
        return False

    otp_obj.attempt_count += 1
    otp_obj.last_attempt_at = timezone.now()
    otp_obj.save(update_fields=["attempt_count", "last_attempt_at"])

    if otp_obj.otp == otp_input:
        user.is_verified = True
        user.save(update_fields=["is_verified"])
        otp_obj.is_used = True
        otp_obj.save(update_fields=["is_used"])
        return True
    return False
