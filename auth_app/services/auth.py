from django.contrib.auth.hashers import make_password
from django.db import IntegrityError


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, data):
        if self.user_repository.exists_by_email(data.get("email")):
            raise ValueError("A user with this email already exists.")
        username = data.get("username")
        if username and self.user_repository.exists_by_username(username):
            raise ValueError("A user with this username already exists.")

        # Извлекаем сырой пароль, хешируем его и кладем обратно в данные
        raw_password = data.get("password")
        if not raw_password:
            raise ValueError("Password is required.")

        data["password"] = make_password(raw_password)
        try:
            return self.user_repository.create(**data)
        except IntegrityError as exc:
            raise ValueError(
                "Unable to register user. "
                "Email or username may already exist."
            ) from exc
