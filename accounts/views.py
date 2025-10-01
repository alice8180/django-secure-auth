from django.http import Http404
from django.utils.decorators import method_decorator # api te direct decorator use korle error dei tai aitar moddhe decorator use korte hobe

# import rest_framework hare
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import authenticate
from rest_framework import status


# exceptions and errors
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError as DRFValidationError


# import simple jwt token 
from rest_framework_simplejwt.tokens import RefreshToken

# import serializers hare 
from accounts.serializers import CreateAccountSerializer
from accounts.serializers import LoginUserSerializer
from accounts.serializers import DummySerializer
from accounts.serializers import ChangePasswordSerializer
from accounts.serializers import ValidateEmailSerializer
from accounts.serializers import ProfileSerializer


# import custom class or functions
from utils.generic_api_view import PublicGenericAPIView
from notifications.services import send_verification_mail
from utils.generate import EncodeDecodeOneTimePasswd # one time url generator for forget password
from accounts.helper import validate_refresh_token
from accounts.helper import generate_one_time_url, validate_one_time_url

# import models hare
from accounts.models import CustomUser
from accounts.models import EmailVerificationToken

# import cookie handler
from accounts.set_cookies import CookieHandler

# import brute force protection
from django_ratelimit.decorators import ratelimit

# import celery task hare
from celery_tasks.notifications import send_celery_mail

# spectacular for auto docs
from drf_spectacular.utils import extend_schema

# import logger 
from utils.logger import accounts_log_info, accounts_log_warning, accounts_log_error, accounts_log_debug




# Create your views here.



"""common errors workflow"""
default_error = Response({"errors": "something was wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Set CSRF token in cookie
@extend_schema(tags=["CSRFToken"])
class GetCsrfToken(PublicGenericAPIView):
    """
    GetCsrfToken is a public API for retrieving a CSRF token.

    - This API uses a **GET request**
    - When you call this API, a **CSRF token will be automatically set in your browser cookie**
    - The CSRF token is required for all unsafe requests such as **POST, PUT, PATCH, DELETE**
    - This improves security and prevents Cross-Site Request Forgery (CSRF) attacks
    - Rate Limit: Maximum 10 requests per minute per IP

    Example Response:
    {
        "message": "csrf token adding in cookie successfully!!"
    }

    Note:
    - The CSRF token will not appear in the response body
    - It will be stored securely in your browser cookie
    """
    
    serializer_class = DummySerializer
    
    @method_decorator(ratelimit(key="ip", rate="10/m", method="GET", block=True))
    def get(self, request):
        response = Response({"message": "csrf token adding in cookie successfully!!"}, status=status.HTTP_200_OK)
        cookie = CookieHandler(request=request, user=None, response=response)        
        cookie.set_csrf_token()
        
        accounts_log_info("CSRF Token set successfully!!", request=request)
        return cookie.get_response()




# create account
@extend_schema(tags=["Accounts"])
class CreateAccount(PublicGenericAPIView):
    """
    CreateAccount is a public API for user registration.

    - This API uses a **POST request**
    - Send your account details (e.g., email, password, name) in the request body
    - If valid, a new user account will be created
    - Returns a success message and account information
    - If invalid, returns validation errors
    """

    serializer_class = CreateAccountSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                accounts_log_info(message=f"account create successfully, {serializer.data}", request=request)
                return Response({"message": "account create successfully!!", "info": serializer.data}, status=status.HTTP_200_OK)

            accounts_log_warning(message="invalid user info", request=request)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            accounts_log_error(message=f"Problem in Create Account API | {str(e)}", request=request)
            return default_error
        



# Resend verification mail api
@extend_schema(tags=["Accounts"])
class ResendVerifyEmail(PublicGenericAPIView):
    """
    ResendVerifyEmail is a public api for email verification token
    
    - This api using POST request
    - Use this api and post your email address
    - Then check your mail box , and you see a new mail from our site
    - Click the url and verify your account
    
    """
    serializer_class = ValidateEmailSerializer
    
    @method_decorator(ratelimit(key="ip", rate="1/m", method="POST", block=True))
    def post(self, request):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                user = serializer.validated_data.get("user")
                if user.is_verified:
                    return Response({"message": "user already verified!!"})

                url = generate_one_time_url(user=user, base_url="/verify-email/")
                send_verification_mail(user=user, subject="Please verify your email to activate your account", url=url, template="emails/resend_verify_email.html", request=request)
                return Response({"Message": "Check your Mail box , you have a new email for verify email"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            accounts_log_error(message=f"Error in ResendVerifyEmail api | {str(e)}", request=request)
            return default_error



# verify Email account api
@extend_schema(tags=["Accounts"])
class VerifyEmail(PublicGenericAPIView):
    """
    VerifyEmail is a public API for account verification.

    - Accepts POST request with <token> in URL
    - If token valid → user verified
    - If token invalid/expired → error returned
    """
    serializer_class = DummySerializer
    
    def post(self, request, token):
        try:
            token_obj = get_object_or_404(EmailVerificationToken, token=token)
            user = validate_one_time_url(user=token_obj.user, token=token_obj)
            send_celery_mail.delay(user.email, "Your account has been successfully verified", "success_template/verify_success.html", {"first_name": user.first_name, "login_url": "http://127.0.0.1:8000/login/"} )
            return Response({"message": "Account Verify successfully!!"}, status=status.HTTP_200_OK)
    
        except Http404:
            return Response({"Invalid_url": "url modified"}, status=status.HTTP_400_BAD_REQUEST)
        
        except DRFValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            accounts_log_error(message=f"Problem in VerifyEmail api | {str(e)}", request=request)
            return default_error
        



# user login api
@extend_schema(tags=["Login-Logout"])
class LoginGenericAPIView(PublicGenericAPIView):
    """
    LoginGenericAPIView is a public API for user authentication.

    - This API uses a **POST request**
    - Send your email and password in the request body
    - If valid and the user is active & verified:
        - A new **access token** and **refresh token** are set in cookies
        - A new **CSRF token** is also set
        - Returns a success message
    - If invalid, returns error messages
    - Rate Limit: Maximum 5 requests per minute per IP
    """
    serializer_class = LoginUserSerializer
    
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        try:
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data.get("email")
                password = serializer.validated_data.get("password")
                user = authenticate(request=request, email=email, password=password)
                if not user:
                    accounts_log_warning(message="Invalid user trying to login", request=request)
                    return Response({"errors": "invalid email and password"}, status=status.HTTP_400_BAD_REQUEST)

                if user and user.is_active and user.is_verified:
                                        
                    refresh = RefreshToken.for_user(user=user)
                    response = Response({"message": "Login successfully"}, status=status.HTTP_200_OK)
                    cookie = CookieHandler(request=request, user=user, response=response)
                    cookie.set_access_token(str(refresh.access_token))
                    cookie.set_refresh_token(str(refresh))
                    cookie.set_last_login()
                    cookie.set_csrf_token()
                    
                    accounts_log_info(message="User Login Successfully", request=request, user=user)
                    return cookie.get_response()
                
                accounts_log_warning(message="this user i think not verified or active , user trying to login but he can't ", request=request, user=user )
                return Response({"errors": "user not verified or not active please verify your account"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        except Exception as e:
            accounts_log_error(message=f"Problem in LoginGenericAPIView API | {str(e)}", request=request)
            return default_error



# get new access token
@extend_schema(tags=["Login-Logout"])
class GetAccessTokenGenericAPIView(PublicGenericAPIView):

    """
    GetAccessTokenGenericAPIView is a public API to refresh the access token.

    - This API uses a **POST request**
    - It checks for the **refresh token** in cookies
    - If valid, a new **access token** is generated and set in cookies
    - Returns a success message
    - If missing or invalid, returns an error
    """
    serializer_class = DummySerializer
    
    def get(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return Response({"errors": "not refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh_token = validate_refresh_token(refresh_token=refresh_token, request=request)
            access_token = str(refresh_token.access_token)
            
            resp0nse = Response({"message": "New access token set successfully!!"}, status=status.HTTP_200_OK) 
            cookie = CookieHandler(request=request, user=None, response=resp0nse)
            cookie.set_access_token(access_token=access_token)
            return cookie.get_response()

        except AuthenticationFailed as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return default_error



@extend_schema(tags=["Login-Logout"])
class LogoutGenericAPIView(GenericAPIView):
    """
    LogoutGenericAPIView is a public API for logging out users.

    - This API uses a **GET request**
    - It removes all authentication cookies (**access, refresh, csrf**) from the browser
    - Returns a success message
    """
    serializer_class = DummySerializer
    
    def get(self, request):
        try:
            user = request.user
            response = Response({"message": "Logout successfully!!"}, status=status.HTTP_200_OK)
            cookie = CookieHandler(request=request, user=user, response=response)
            cookie.delete_token()
            return cookie.response
        except Exception as e:
            return default_error



"""Spectacular APIView"""
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny


class PublicSchemaView(SpectacularAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
class PublicRedocView(SpectacularRedocView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
class PublicSwaggerView(SpectacularSwaggerView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    
    


# forget password
@extend_schema(tags=["ForgetPassword"])
class ForgetPasswordGenericAPIView(PublicGenericAPIView):
    """
    ResetPasswordGenericAPIView is a public API for requesting a password reset.

    - This API uses a **POST request**
    - Send your email address in the request body
    - If the email exists, a reset link will be sent to your inbox
    - Click the link to set a new password
    """
    serializer_class = ValidateEmailSerializer
    
    def post(self, request):
        try:
            
            data = request.data
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                user = serializer.validated_data.get("user")
                
                # generate toke + uuid 
                encode = EncodeDecodeOneTimePasswd(request=request)
                reset_url = encode.generate_url_reset_password(user=user, url="/set-new-password/")

                send_verification_mail(user=user, subject="Reset your account password", url=reset_url, template="emails/set_new_password.html")
                return Response({"message": "Check your mail box and open the url for set new password!!"}, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return default_error
        


# set new password 
@extend_schema(tags=["ForgetPassword"])
class SetNewPasswordGenericAPIView(PublicGenericAPIView):
    """
    SetNewPasswordGenericAPIView is a public API for setting a new password.

    - This API uses a **POST request**
    - Requires a valid `uuid64` and `token` from the password reset link
    - Send your new password in the request body
    - If valid, your password will be updated successfully
    """
    
    serializer_class = ChangePasswordSerializer
    
    def post(self, request, uuid64, token):
        
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                password = serializer.validated_data.get("password")
                
                decode = EncodeDecodeOneTimePasswd(request=request)
                user = decode.decode_password_reset_url(uuid64=uuid64, token=token).get("user")

                user.set_password(password)
                user.save()
                print("celery mail check 1")
                send_celery_mail.delay(user.email, "Your password has been changed successfully" , "success_template/password_change_successful.html", {"first_name": user.first_name})
                print("celery mail check 1")

                return Response({"message": "Password change successfully!!"}, status=status.HTTP_200_OK)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
        except DRFValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            accounts_log_error(message=f"problem on SetNewPasswordGenericAPIView | {str(e)}", request=request)
            return default_error
        
        
        
@extend_schema(tags=["Accounts"])
class ManageUserProfileGenericAPIView(GenericAPIView):
    """
    ManageUserProfileGenericAPIView is an API for viewing and updating user profile.

    - **GET request** → Returns the authenticated user's profile data
    - **PATCH request** → Update specific profile fields (e.g., phone, gender, etc.)
    - Requires authentication
    """
    
    serializer_class = ProfileSerializer
    
    def get(self, request):
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile)
            return Response({"profile": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            accounts_log_error(message=f"problem on ManageAccountGenericAPIView get method | {str(e)}", request=request, user=request.user)
            return default_error
        
    def patch(self, request):
        try:
            data = request.data
            profile = request.user.profile
            serializer = self.get_serializer(profile, data=data, partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "profile update successfully!!", "info": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            accounts_log_error(f"problem on ManageAccountGenericAPIView patch method | {str(e)}", request=request, user=request.user)
            return default_error




class TestView(GenericAPIView):
    
    def get(self, request):
        return Response({"message": "get request successfully"}, status=status.HTTP_200_OK)
        
