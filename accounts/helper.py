from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed
# from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.exceptions import ValidationError 

from rest_framework.exceptions import ValidationError as DRFValidationError
from accounts.models import EmailVerificationToken
from accounts.models import CustomUser
from django.http import Http404
from django.conf import settings
from utils.constants import JWT_ERROR_MESSAGES
from utils.logger import accounts_log_warning, accounts_log_info


def validate_refresh_token(refresh_token: str, request=None, user=None) -> RefreshToken:
    """
    Validate the given refresh token string.
    Raise AuthenticationFailed with proper messages if invalid.
    """
    try:
        token = RefreshToken(refresh_token)
        return token
    except InvalidToken:
        accounts_log_warning(message="Invalid refresh_token", request=request, user=user)
        raise AuthenticationFailed(JWT_ERROR_MESSAGES["invalid_token"])
    except TokenError:
        accounts_log_warning(message="Tampered/modified refresh_token", request=request, user=user)
        raise AuthenticationFailed({"Invalid token": "Expired Refresh token"})
    except Exception as e:
        accounts_log_warning(message=f"Unexpected error in validate_refresh_token | {str(e)}", request=request, user=user)
        raise AuthenticationFailed(JWT_ERROR_MESSAGES["unexpected"])







import secrets
from django.utils.timezone import now
from datetime import timedelta
from accounts.models import EmailVerificationToken

def generate_one_time_url(user, base_url="/verify-email/") -> str:
    """
    Generate a secure one-time verification URL for the given user.

    - Creates a random cryptographically secure token.
    - Stores it in the `EmailVerificationToken` table with a 30 min expiry.
    - Returns a full URL ready to be sent via email.
    """
    token = secrets.token_urlsafe(32)  # Secure random token
    expiry = now() + timedelta(minutes=30)  # Token valid for 30 minutes

    EmailVerificationToken.objects.create(user=user, token=token, expired_at=expiry)

    domain = settings.FRONTEND_URL.rstrip("/")  # Remove trailing slash
    return f"{domain}{base_url}{token}/"



def validate_one_time_url(user: object, token: object):
    """
    Validate and consume a one-time verification token.
    """
    if not token.is_valid():
        raise DRFValidationError({"error": "Invalid or expired link"})

    token.is_used = True
    token.save(update_fields=["is_used"])

    user.is_verified = True
    user.save(update_fields=["is_verified"])

    return user
