from users import views
from django.urls import path


urlpatterns = [
    path(route="sign-up/", view=views.UserCreateAPIView.as_view(), name="UserCreate"),
    path(route="<int:pk>/update/", view=views.UserUpdateAPIView.as_view()),
    path(route="change-password/", view=views.ChangePasswordAPIView.as_view()),
    path(route="token/", view=views.ObtainAuthTokenAPIView.as_view()),
    path(route="list/", view=views.UserListAPIView.as_view()),
    path(route="send-otp/", view=views.SendOTPAPIView.as_view()),
    path(route="reset-password/", view=views.ResetPasswordAPIView.as_view()),
]
