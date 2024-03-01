
from base.serializers import DynamicFieldsModelSerializer
from app.models import User


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        # use 'fields = "__all__"' if all fields needed
        fields = ["first_name", "last_name", "email"]
