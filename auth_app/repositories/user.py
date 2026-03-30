class UserRepository:
    def __init__(self, model):
        self.model = model  # модель передается через конструктор

    def create(self, **data):
        return self.model.objects.create(**data)

    def get_by_id(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def get_by_email(self, email):
        return self.model.objects.filter(email=email).first()

    def exists_by_email(self, email: str) -> bool:
        return self.model.objects.filter(email=email).exists()

    def exists_by_username(self, username: str) -> bool:
        return self.model.objects.filter(username=username).exists()

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
