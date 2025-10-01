from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.http import Http404, HttpRequest
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser

# import logger hare
from utils.logger import accounts_log_debug, accounts_log_info, accounts_log_warning, accounts_log_error




class EncodeDecodeOneTimePasswd:
    """
    Helper class for generating and decoding password reset URLs
    with token verification.
    """

    def __init__(self, request: HttpRequest):
        self.request = request

    def generate_url_reset_password(self, user: object, url: str) -> str:
        """
        Generate a password reset URL with UUID and token for the given user.
        """
        try:
            uuid64 = urlsafe_base64_encode(force_bytes(str(user.uuid)))
            token = PasswordResetTokenGenerator().make_token(user)

            domain = settings.FRONTEND_URL.rstrip("/")  # remove trailing slash if exists
            reset_url = f"{domain}{url}{uuid64}/{token}/"
            accounts_log_info(message=f"ResetPassword one time url generate successfully!!", request=self.request, user=user)
            return reset_url

        except Exception as e:
            accounts_log_error(message=f"Failed to generate password reset URL | {str(e)}", user=user)
            raise Exception("Internal server error while generating reset URL.")


    def decode_password_reset_url(self, uuid64: str, token: str) -> dict:
        """
        Decode the password reset URL, validate the user and token.
        """
        try:
            uuid = force_str(urlsafe_base64_decode(uuid64))
            user = get_object_or_404(CustomUser, uuid=uuid)

            # Validate token
            if not PasswordResetTokenGenerator().check_token(user, token):
                accounts_log_warning(message="Invalid or expired password reset token.", user=user)
                raise ValidationError({"errors": "Invalid or expired token"})

            accounts_log_info(message="ResetPassword URL verify successfully.", request=self.request, user=user)
            return {"user": user, "is_verified": True}

        except Http404:
            accounts_log_warning(message="User not found for given UUID.", request=self.request, user=None)
            raise ValidationError({"errors": "User not found"})

        except ValidationError:
            raise

        except Exception as e:
            accounts_log_error(message=f"Unexpected error during token decoding | {str(e)}", request=self.request, user=None,)
            raise Exception("Internal server error while decoding reset token.")

