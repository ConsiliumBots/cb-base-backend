from rest_framework import permissions
from rest_framework_simplejwt.backends import TokenBackend
from app.models import User


def request_to_user(request):
    """
    gets user from request by JWT token.
    """
    try:
        token = request.META.get("HTTP_AUTHORIZATION")
        user_id = TokenBackend(algorithm="HS256").decode(
            token, verify=False)["user_id"]
        return User.objects.get(id=user_id)
    except:
        return None


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request_to_user(request)
        return user != None
