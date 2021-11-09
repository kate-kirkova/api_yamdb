from rest_framework import permissions


class UserAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.method in ['GET', 'PATCH']

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or (request.obj.username == request.user.username) 

class AdminLevelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == 'admin'
        return False


class AdminLevelOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )
