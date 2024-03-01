
from base.serializers import DynamicFieldsModelSerializer
from app.models import Post


class PostSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Post
        # use 'fields = "__all__"' if all fields needed
        fields = ["content", "user"]
