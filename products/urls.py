from django.urls import path
from products import views


urlpatterns = [
    path(route="create/", view=views.ProductCreateAPIView.as_view()),
    path(route="list/", view=views.ProductListAPIView.as_view()),
    path(route="<int:pk>/", view=views.ProductRetrieveAPIView.as_view()),
    path(route="<int:pk>/update/", view=views.ProductUpdateAPIView.as_view()),
    path(route="<int:pk>/delete/", view=views.ProductDestroyAPIView.as_view()),
    path(route="<int:pk>/comments/create/", view=views.CommentCreateAPIView.as_view()),
    path(route="<int:pk>/comments/list/", view=views.CommentListAPIView.as_view()),
    path(route="comments/<int:pk>/delete/", view=views.CommentDestroyAPIView.as_view()),
]
