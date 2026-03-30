from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError

from core.token import generate_token


class AuthService:
    def __init__(self, user_repository, session_repository=None):
        self.user_repository = user_repository
        self.session_repository = session_repository

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

    def login(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise ValueError("Email and password are required.")

        user = self.user_repository.get_by_email(email)
        if not user or not user.is_active:
            raise ValueError("Invalid email or password.")

        if not check_password(password, user.password):
            raise ValueError("Invalid email or password.")

        if self.session_repository is None:
            raise ValueError("Session repository is required for login.")

        token = generate_token()
        return self.session_repository.create(user=user, token=token)
