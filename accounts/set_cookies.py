from django.conf import settings
from django.middleware.csrf import get_token
from django.http import HttpRequest

# import rest_framework
from rest_framework.response import Response
from rest_framework import status


# import simpleJWT
from rest_framework_simplejwt.tokens import RefreshToken


# import other classes or functions
from typing import Optional

# import logger hare

from utils.logger import accounts_log_debug, accounts_log_info, accounts_log_warning, accounts_log_error

# create your cookie handler hare 




class CookieHandler():
    
    def __init__(self, request:HttpRequest, user:object=None, response:Response=None):
        self.request = request
        self.user = user
        self.response = response or Response(status=status.HTTP_200_OK)
    
        
        
    def _common_settings (self) -> dict:
        
        return {
            "httponly":True,
            "samesite":settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE"),
            "secure":settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE"),
            "path":settings.SIMPLE_JWT.get("AUTH_COOKIE_PATH")
        }
    
    
    
    def set_access_token(self, access_token) -> None:
        try:
            self.response.set_cookie(
                key=settings.SIMPLE_JWT.get("AUTH_COOKIE"),
                value=access_token,
                **self._common_settings()
            )
            accounts_log_info("Access Token Set Successfully", request=self.request, user=self.user)
        except Exception as e:
            accounts_log_error(message=f"Access token can't set | {str(e)}", request=self.request, user=self.user)
            raise Exception(f"Problem on set_access_token | {str(e)}")
        
        
    
    def set_refresh_token(self, refresh_token) -> None:
        try:
            self.response.set_cookie(
                key=settings.SIMPLE_JWT.get("AUTH_COOKIE_REFRESH"),
                value=refresh_token,
                **self._common_settings()
            )
            accounts_log_info(message=f"RefreshToken set successfully!!", request=self.request, user=self.user)
        except Exception as e:
            accounts_log_error(message=f"RefreshToken cat't set | {str(e)}", request=self.request, user=self.user)
            raise Exception(f"Problem on set_refresh_token | {str(e)}")
        
        
        
    def set_csrf_token(self) -> None:
        try:
            csrf_token = get_token(request=self.request)
            self.response.set_cookie(
                key=settings.CSRF_COOKIE_NAME,
                value=csrf_token,
                
                httponly=False, # False jate React/JS theke access korte pare :)
                samesite=settings.SIMPLE_JWT.get("AUTH_COOKIE_SAMESITE"),
                secure=settings.SIMPLE_JWT.get("AUTH_COOKIE_SECURE"),
                path=settings.SIMPLE_JWT.get("AUTH_COOKIE_PATH"),
            )
            accounts_log_info(message=f"CSRF Token set successfully!!", request=self.request, user=self.user)
                    
        except Exception as e:
            accounts_log_error(message=f"CSRF Token cat't set | {str(e)}", request=self.request, user=self.user)
            raise Exception(f"Problem on set_csrf_token | {str(e)}")




    def set_last_login(self):
        from django.contrib.auth.models import update_last_login
        update_last_login(sender=None, user=self.user)




    def delete_token(self):
        try:
            refresh_token = self.request.COOKIES.get("refresh_token")
            if refresh_token:
                try:
                    RefreshToken(refresh_token).blacklist()
                except Exception as e:
                    accounts_log_error(message=f"Refresh token not found in user cookie, tar porew user ai jaigai kivabe ", request=self.request, user=self.user)
                    raise Exception(f"Refresh Token not found | {str(e)}")

            response = self.response
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            response.delete_cookie("csrftoken")
            accounts_log_info(message=f"Delete all tokens in the cookies!!", request=self.request, user=self.user)
            
        except Exception as e:
            accounts_log_error(message=f"Can't delete tokens in the cookie | {str(e)}", request=self.request, user=self.user)
            raise Exception(f"Problem on delete_token | {str(e)}")

        
    def get_response(self) -> Response:
        return self.response