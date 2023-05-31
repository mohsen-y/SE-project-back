from rest_framework.permissions import BasePermission
from products import models


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj: models.Comment):
        return obj.author == request.user
