from rest_framework.permissions import BasePermission


class IsPartner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_partner', False)
