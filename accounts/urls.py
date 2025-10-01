from django.urls import path
from accounts import views


# create your urls
urlpatterns = [
    path("test-api/", views.TestView.as_view(), name="test_api"),
    
    path("get-csrf-token/", views.GetCsrfToken.as_view(), name="get_csrf_token_generic_api_view"),
    path("create-account/", views.CreateAccount.as_view(), name="create_account_generic_api_view"),
    
    # verify email
    path("resend-verify-email/", views.ResendVerifyEmail.as_view(), name="resend_verify_email_public_generic_api_view"),
    path("verify-email/<str:token>/", views.VerifyEmail.as_view(), name="verify_email_public_generic_api_view"),
    
    # login, logout apis    
    path("login/", views.LoginGenericAPIView.as_view(), name="login_generic_api_view"),
    path("logout/", views.LogoutGenericAPIView.as_view(), name="logout_generic_api_view"),
    
    # get new access token 
    path("get-new-access-token/", views.GetAccessTokenGenericAPIView.as_view(), name="get_new_access_token_generic_api_view"),

    # reset password urls
    path("forget-password/", views.ForgetPasswordGenericAPIView.as_view(), name="reset_password_generic_api_view"),
    path("set-new-password/<str:uuid64>/<str:token>/", views.SetNewPasswordGenericAPIView.as_view(), name="set_new_password_generic_api_view"),

    # manage user profile
    path("profile/", views.ManageUserProfileGenericAPIView.as_view(), name="profile_generic_api_view"),


]
