from base.views import BaseViewSet
from app.models import User
from app.serializers import UserSerializer
from app.permissions import IsSuperUser


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get"]
    permission_classes = [IsSuperUser]  # only super users can access

    def get_queryset(self):
        return super().get_queryset()

    def retrieve(self, request, pk=None):
        """
        Get a single user.
        """
        return super().retrieve(request, pk=pk)

    def list(self, request, *args, **kwargs):
        """
        List users.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create user.
        """
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, pk=None):
        """
        Update user.
        """
        return super().partial_update(request, pk=pk)

    def destroy(self, request, pk=None):
        """
        Delete user.
        """
        return super().destroy(request, pk=pk)
