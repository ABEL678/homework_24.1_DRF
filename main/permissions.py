from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import UserRoles


class IsModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == UserRoles.MODERATOR


class IsCourseOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsCourseOrLessonOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.course.owner == request.user or obj.course.lesson_set.filter(owner=request.user).exists()


class IsPaymentOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
