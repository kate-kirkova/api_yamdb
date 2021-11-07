from rest_framework import permissions


class UserAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or (
            request.obj.username == request.user.username) 

class AdminLevelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser