from users import views as users_views
from django.urls import path


urlpatterns = [
    path(route="sign-up/", view=users_views.UserCreateAPIView.as_view()),
]
