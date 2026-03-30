import pytest
from unittest.mock import MagicMock
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError

from auth_app.services import AuthService


class TestAuthService:
    @pytest.fixture
    def mock_repo(self):
        """Фикстура для создания 'чистого' мока репозитория перед каждым тестом."""
        return MagicMock()

    @pytest.fixture
    def auth_service(self, mock_repo):
        """Фикстура для инициализации сервиса с поддельным репозиторием."""
        return AuthService(user_repository=mock_repo)

    def test_register_user_success(self, auth_service, mock_repo):
        """Проверка успешной регистрации: данные верны, пароль хешируется."""
        # Настройка мока: юзера с такими данными нет
        mock_repo.exists_by_email.return_value = False
        mock_repo.exists_by_username.return_value = False

        # Имитируем возврат созданного объекта (просто строку или Mock)
        fake_user = MagicMock(email="test@mail.com")
        mock_repo.create.return_value = fake_user

        user_data = {
            "email": "test@mail.com",
            "username": "testuser",
            "password": "secure_password_123",
        }

        # Вызов метода
        result = auth_service.register_user(user_data)

        # 1. Проверяем, что вернулся ожидаемый объект
        assert result == fake_user

        # 2. Проверяем, что в репозиторий ушел хеш, а не сырой пароль
        # Достаем аргументы, с которыми был вызван метод create
        args, kwargs = mock_repo.create.call_args
        hashed_password = kwargs["password"]

        assert hashed_password != "secure_password_123"
        # Проверяем валидность хеша через встроенную функцию Django
        assert check_password("secure_password_123", hashed_password)

    def test_register_user_duplicate_email(self, auth_service, mock_repo):
        """Проверка ошибки, если email уже занят."""
        mock_repo.exists_by_email.return_value = True

        user_data = {"email": "exists@mail.com", "password": "123"}

        with pytest.raises(ValueError) as exc:
            auth_service.register_user(user_data)

        assert str(exc.value) == "A user with this email already exists."
        # Проверяем, что до создания дело не дошло
        mock_repo.create.assert_not_called()

    def test_register_user_duplicate_username(self, auth_service, mock_repo):
        """Проверка ошибки, если username уже занят."""
        mock_repo.exists_by_email.return_value = False
        mock_repo.exists_by_username.return_value = True

        user_data = {
            "email": "new@mail.com",
            "username": "busy_name",
            "password": "123",
        }

        with pytest.raises(ValueError) as exc:
            auth_service.register_user(user_data)

        assert str(exc.value) == "A user with this username already exists."

    def test_register_user_integrity_error(self, auth_service, mock_repo):
        """Проверка обработки неожиданной ошибки базы данных (IntegrityError)."""
        mock_repo.exists_by_email.return_value = False
        mock_repo.exists_by_username.return_value = False

        # Имитируем, что проверка прошла, но база в момент записи выкинула ошибку
        mock_repo.create.side_effect = IntegrityError()

        user_data = {"email": "test@mail.com", "password": "123"}

        with pytest.raises(ValueError) as exc:
            auth_service.register_user(user_data)

        assert "Unable to register user" in str(exc.value)
