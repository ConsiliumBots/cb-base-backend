from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from app.serializers import UserSerializer
from app.models import User
from django.http import JsonResponse
from rest_framework.exceptions import PermissionDenied


@api_view(["POST"])
def login(request):

    # get data
    data = request.data

    # get email, password
    email, password = data['username'], data['password']

    # get user
    user = User.objects.get(email=email)
    if user.check_password(password):

        # refresh token
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        data = {'access': str(refresh), 'user': user_serializer.data}
        return JsonResponse(data=data)
    raise PermissionDenied()
