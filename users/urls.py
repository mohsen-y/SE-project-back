from rest_framework.authtoken import views as authtoken_views
from users import views as users_views
from django.urls import path


urlpatterns = [
    path(route="sign-up/", view=users_views.UserCreateAPIView.as_view()),
    path(route="<int:pk>/", view=users_views.UserUpdateAPIView.as_view()),
    path(route="change-password/", view=users_views.ChangePasswordAPIView.as_view()),
    path(route="token/", view=authtoken_views.obtain_auth_token),
    path(route="", view=users_views.UserListAPIView.as_view()),
    path(route="send-otp/", view=users_views.SendOTPAPIView.as_view()),
    path(route="reset-password/", view=users_views.ResetPasswordAPIView.as_view()),
]
