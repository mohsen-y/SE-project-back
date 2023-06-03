from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from users.permissions import IsUserCreator
from rest_framework.request import Request
from rest_framework.views import APIView
from django.core.mail import send_mail
from users import serializers, models
from rest_framework import status
import random

class UserCreateAPIView(CreateAPIView):
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [AllowAny]


class UserListAPIView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(UpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsUserCreator]


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.ChangePasswordSerializer)
    def put(self, request: Request, format=None):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.password = make_password(serializer.data.get("password"))
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendOTPAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializers.SendOTPSerializer)
    def put(self, request: Request, format=None):
        serializer = serializers.SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = models.User.objects.get(email=serializer.data.get("email"))
        except models.User.DoesNotExist:
            return Response(
                data={"detail": "Email not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        code = str(random.randint(100000, 999999))
        send_mail(
            subject="Reset Password OTP",
            message=f"Your OTP: {code}",
            from_email="store.shoe@info.com",
            recipient_list=[user.email],
        )
        models.OTP.objects.update_or_create(
            defaults={
                "user": user,
                "code": code,
            },
            user=user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=serializers.ResetPasswordSerializer)
    def put(self, request: Request, format=None):
        serializer = serializers.ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = models.User.objects.get(email=serializer.data.get("email"))
        except models.User.DoesNotExist:
            return Response(
                data={"detail": "Email not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            otp = models.OTP.objects.get(user=user)
            if not otp.is_valid() or otp.code != serializer.data.get("code"):
                raise models.OTP.DoesNotExist
        except models.OTP.DoesNotExist:
            return Response(
                data={"detail": "Incorrect otp."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp.delete()
        user.password = make_password(serializer.data.get("password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ObtainAuthTokenAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = {
            "id": user.pk,
            "last_login": user.last_login,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "date_joined": user.date_joined,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "role": user.role,
            "zip_code": user.zip_code,
            "national_id": user.national_id,
            "token": token.key,
        }
        return Response(data=data)
