from base.views import BaseViewSet
from app.models import Post
from app.serializers import PostSerializer
from app.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class PostViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]  # only super users can access

    def get_queryset(self):
        """
        Get all posts from user.
        """
        return self.user.posts.all()

    def retrieve(self, request, pk=None):
        """
        Get a single post.
        """
        return super().retrieve(request, pk=pk)

    def list(self, request, *args, **kwargs):
        """
        List posts.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create post.
        """
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, pk=None):
        """
        Update post. User can only update own posts.
        """
        post = Post.objects.get(pk=pk)
        if post.user != self.user:
            raise PermissionDenied()
        return super().partial_update(request, pk=pk)

    def destroy(self, request, pk=None):
        """
        Delete post. User can only destroy own posts.
        """
        post = Post.objects.get(pk=pk)
        if post.user != self.user:
            raise PermissionDenied()
        return super().destroy(request, pk=pk)
