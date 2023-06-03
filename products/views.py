from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from products.permissions import IsCommentAuthor
from users.permissions import IsOwner, IsAdmin
from products import models, serializers


class ProductCreateAPIView(CreateAPIView):
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]


class ProductListAPIView(ListAPIView):
    # TODO: Filters
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]


class ProductRetrieveAPIView(RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]


class ProductUpdateAPIView(UpdateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]


class ProductDestroyAPIView(DestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]


# TODO: Rate Product


class CommentCreateAPIView(CreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentListAPIView(ListAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [AllowAny]


class CommentDestroyAPIView(DestroyAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]
