"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path, path, include
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi


schema_view = get_schema_view(
    info=openapi.Info(
        title="SE Project",
        default_version="0.1",
    ),
    url="http://127.0.0.1:8000/",
    public=True,
    authentication_classes=None,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        route=r"^swagger/$",
        view=schema_view.with_ui(),
        name="schema-swagger-ui",
    ),
    path(route="users/", view=include("users.urls")),
    path(route="products/", view=include("products.urls")),
]
