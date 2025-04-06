from rest_framework.permissions import BasePermission

class IsAdminManagerOrOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager', 'owner']

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin']


class IsAdminOrOwnerOfStadium(BasePermission):
    """
    Admin barcha stadionni o‘chira oladi,
    Owner faqat o‘zinikini,
    Manager umuman o‘chira olmaydi
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and (
                user.role == 'admin' or
                (user.role == 'owner' and obj.owner == user)
            )
        )