from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from users import serializers, models

class UserCreateAPIView(CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListAPIView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]
