from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        if obj != request.user:
            raise PermissionDenied("Вы не можете редактировать чужого пользователя!")
        return obj == request.user
