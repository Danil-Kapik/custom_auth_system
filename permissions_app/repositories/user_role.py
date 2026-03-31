class UserRoleRepository:
    def __init__(self, model):
        self.model = model

    def get_role_ids_for_user(self, user_id):
        if user_id is None:
            return []

        return list(
            self.model.objects.filter(user_id=user_id)
            .values_list("role_id", flat=True)
            .distinct()
        )

    def get_role_ids_for_user_object(self, user):
        return self.get_role_ids_for_user(getattr(user, "pk", None))
