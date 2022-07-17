from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsOwnerOrStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or request.user.id == 0
            or request.method in permissions.SAFE_METHODS
        )


class IsRoleAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_admin
            or user.is_superuser
        )


class IsRoleModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_moderator
            or user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.is_moderator
            or user.is_staff
        )
