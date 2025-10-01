from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

# permission class or functions
from accounts.permissions import IsOwner

# other class and logic
from accounts.csrf_authentication import CsrfAuthentication

# create public api view

class PublicGenericAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfAuthentication]
    
