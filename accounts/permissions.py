
from rest_framework.permissions import BasePermission


# create your permissions hare 


# basic permission not spacial :), only owner can access
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user or request.user.is_superuser:
            return True
        return False