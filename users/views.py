from rest_framework.generics import CreateAPIView, ListAPIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.core.mail import send_mail
from users import serializers, models
from rest_framework import status
import random

class UserCreateAPIView(CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListAPIView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = [AllowAny]


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
