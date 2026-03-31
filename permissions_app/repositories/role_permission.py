class RolePermissionRepository:
    def __init__(self, model):
        self.model = model

    def has_permission(self, role_ids, permission_code):
        if not role_ids or not permission_code:
            return False

        return self.model.objects.filter(
            role_id__in=role_ids,
            permission__code=permission_code,
        ).exists()

    def get_permission_codes_for_roles(self, role_ids):
        if not role_ids:
            return []

        return list(
            self.model.objects.filter(role_id__in=role_ids)
            .values_list("permission__code", flat=True)
            .distinct()
        )
