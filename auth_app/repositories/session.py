class SessionRepository:

    def __init__(self, model):
        self.model = model  # модель передается через конструктор

    def create(self, **data):
        return self.model.objects.create(**data)

    def get_by_id(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def get_by_token(self, token):
        return self.model.objects.filter(token=token).first()

    def filter(self, **filters):
        return self.model.objects.filter(**filters)

    def list(self, **filters):
        return self.model.objects.filter(**filters).order_by("-created_at")

    def update(self, instance, **data):
        if not data:
            return instance

        for field, value in data.items():
            setattr(instance, field, value)
        instance.save(update_fields=list(data.keys()))
        return instance

    def delete(self, instance):
        instance.delete()

    def delete_by_token(self, token):
        return self.model.objects.filter(token=token).delete()

    def delete_by_user(self, user):
        return self.model.objects.filter(user=user).delete()
