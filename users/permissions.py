from rest_framework.permissions import BasePermission


class UserViewSetPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ('update', 'partial_update'):
            return request.user == obj
        return True
