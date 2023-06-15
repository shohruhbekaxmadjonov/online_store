from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object
        return obj.owner == request.user


class IsSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to perform certain actions.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser
