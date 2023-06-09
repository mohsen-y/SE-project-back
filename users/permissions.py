from rest_framework.permissions import BasePermission
from users import models


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == models.User.Role.OWNER:
            return True

        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == models.User.Role.ADMIN:
            return True

        return False


class IsUserCreator(BasePermission):
    def has_object_permission(self, request, view, obj: models.User):
        return obj.id == request.user.id
