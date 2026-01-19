from rest_framework.permissions import BasePermission


class IsMonitoringUser(BasePermission):
    """
    Пускаем только тех, у кого есть профиль мониторинга.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and hasattr(user, "monitoring_profile")
        )
