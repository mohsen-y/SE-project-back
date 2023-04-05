from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from users import serializers


class UserCreateAPIView(CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [AllowAny]
