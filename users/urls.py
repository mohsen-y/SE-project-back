from rest_framework.authtoken import views as authtoken_views
from users import views as users_views
from django.urls import path


urlpatterns = [
    path(route="sign-up/", view=users_views.UserCreateAPIView.as_view()),
    path(route="token/", view=authtoken_views.obtain_auth_token),
]
