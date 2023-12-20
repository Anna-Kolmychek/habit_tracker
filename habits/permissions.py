from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Object-level permission to only owners"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
