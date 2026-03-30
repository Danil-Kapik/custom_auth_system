from django.db import models


class User(models.Model):
    EMAIL_MAX_LENGTH = 255
    NAME_MAX_LENGTH = 150

    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        help_text="Адрес электронной почты пользователя (в качестве логина)",
    )
    username = models.CharField(
        max_length=NAME_MAX_LENGTH,
        unique=True,
        help_text="Обязательно, не более 150 символов.",
    )
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH, blank=True)
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Указывает, может ли данный пользователь войти в систему.",
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Метка мягкого удаления пользователя.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "auth_user"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class Session(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    token = models.CharField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "auth_session"
        ordering = ["-created_at"]

    def __str__(self):
        return f"session:{self.id} user:{self.user_id}"
