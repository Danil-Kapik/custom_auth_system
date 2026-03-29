class PermissionRepository:
    def __init__(self, model):
        self.model = model  # модель передается через конструктор

    def create(self, **data):
        return self.model.objects.create(**data)

    def get_by_id(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def get_by_code(self, code):
        return self.model.objects.filter(code=code).first()

    def filter(self, **filters):
        return self.model.objects.filter(**filters)

    def list(self, **filters):
        return self.model.objects.filter(**filters).order_by("code")

    def update(self, instance, **data):
        if not data:
            return instance

        for field, value in data.items():
            setattr(instance, field, value)
        instance.save(update_fields=list(data.keys()))
        return instance

    def delete(self, instance):
        instance.delete()
