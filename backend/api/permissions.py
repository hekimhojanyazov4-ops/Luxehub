from rest_framework import permissions


def _is_staff_role(user):
    return bool(
        user
        and user.is_authenticated
        and user.role in (user.Role.ADMIN, user.Role.MANAGER)
    )


class IsAdminOrManager(permissions.BasePermission):
    """Allows access only to users with ADMIN or MANAGER role."""

    def has_permission(self, request, view):
        return _is_staff_role(request.user)


class IsAdminOrManagerOrReadOnly(permissions.BasePermission):
    """Anyone can read (list/retrieve); only staff roles can write."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return _is_staff_role(request.user)


class IsOwnerOrAdminOrManager(permissions.BasePermission):
    """The owning user, or staff roles, may access/modify the object."""

    owner_field = "user"

    def has_object_permission(self, request, view, obj):
        user = request.user
        if _is_staff_role(user):
            return True
        owner = getattr(obj, self.owner_field, None)
        return owner == user