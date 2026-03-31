class PermissionService:
    def __init__(self, user_role_repo, role_permission_repo):
        self.user_role_repo = user_role_repo
        self.role_permission_repo = role_permission_repo

    def check_permission(self, user, permission_code):
        if user is None:
            return False

        user_id = getattr(user, "pk", None)
        if user_id is None:
            return False

        role_ids = self.user_role_repo.get_role_ids_for_user(user_id)
        if not role_ids:
            return False

        return self.role_permission_repo.has_permission(
            role_ids, permission_code
        )
