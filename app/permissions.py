from rest_framework import permissions
from app.models import User
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from base.permissions import request_to_user
from app.models import Role, UserRole


class IsAuthenticated(permissions.BasePermission):
    """
    Defines wether user is authenticated or not.
    """

    def has_permission(self, request, view):
        user = request_to_user(request)
        return user != None


class IsSuperUser(permissions.BasePermission):
    """
    Defines wether user is super user or not.
    """

    def has_permission(self, request, view):
        user = request_to_user(request)
        if not user:
            return False
        return user.is_superuser


class JWTAuthenticationSafe(JWTAuthentication):
    """
    verifies if user is authenticated through JWT.
    """

    def authenticate(self, request):
        try:
            return super().authenticate(request=request)
        except InvalidToken:
            return None
