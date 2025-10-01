from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import ExpiredTokenError, TokenError, InvalidToken 

# import others 
from typing import Optional
from django.http import HttpRequest

# import logger 
from utils.constants import JWT_ERROR_MESSAGES

from utils.logger import accounts_log_debug, accounts_log_info, accounts_log_warning, accounts_log_error

# create your cookie base auth hare



class CookieJWTAuth(JWTAuthentication):
    """
    Custom JWT Authentication using cookies instead of Authorization header.

    - Reads access_token from request.COOKIES
    - Validates JWT token
    - Ensures user is active & verified
    - Raises AuthenticationFailed for invalid/expired/modified tokens
    """

    def authenticate(self, request:Optional[HttpRequest]) ->tuple:

        access_token = request.COOKIES.get("access_token")
        if not access_token:
            raise AuthenticationFailed(JWT_ERROR_MESSAGES["no_token"])

        try:            
            validated_access_token = self.get_validated_token(raw_token=access_token)
            user = self.get_user(validated_token=validated_access_token)

            if not (user and user.is_active and getattr(user, "is_verified", False)):
                accounts_log_warning(message="inactive or unverified user", request=request)
                raise AuthenticationFailed(JWT_ERROR_MESSAGES["user_inactive"])

            accounts_log_info(f"User is Authenticated!!", request=request, user=user)
            return (user, validated_access_token)


        except InvalidToken as e:
            accounts_log_warning(message="Invalid access_token", request=request)
            raise AuthenticationFailed(JWT_ERROR_MESSAGES["invalid_token"])

        except ExpiredTokenError:
            accounts_log_warning(message="Expired access_token", request=request)
            raise AuthenticationFailed(JWT_ERROR_MESSAGES["token_expired"])

        except TokenError:
            accounts_log_warning(message="Token tampered/modified", request=request)
            raise AuthenticationFailed(JWT_ERROR_MESSAGES["token_error"])

        except Exception as e:
            accounts_log_error(message=f"Unexpected error in CookieJWTAuth | {str(e)}", request=request)
            raise AuthenticationFailed(JWT_ERROR_MESSAGES["unexpected"])
