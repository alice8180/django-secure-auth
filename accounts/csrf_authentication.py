from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.middleware.csrf import CsrfViewMiddleware
from django.core.exceptions import PermissionDenied

# import logger 



# create your csrf authentication hare

class CsrfAuthentication(BasicAuthentication):
    """
    Custom DRF authentication class that enforces CSRF validation.
    This is required when using cookie-based authentication (e.g., JWT in HttpOnly cookies).
    """
    
    def authenticate(self, request):
        csrf_middleware = CsrfViewMiddleware(get_response=lambda req: None)

        try:
            # Run CSRF checks as if this was a normal Django view
            reason = csrf_middleware.process_view(request=request, callback=None, callback_args=(), callback_kwargs={})
        
        except PermissionDenied as exc:
            raise AuthenticationFailed(f"CSRF Failed")

        if reason:
            raise AuthenticationFailed(f"CSRF Failed")

        # Return None because CSRF check doesn't authenticate a user,
        # it only validates request safety
        return None
