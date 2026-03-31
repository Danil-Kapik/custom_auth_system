import pytest
from unittest.mock import MagicMock

from permissions_app.services import PermissionService


class TestPermissionService:
    @pytest.fixture
    def user_role_repo(self):
        return MagicMock()

    @pytest.fixture
    def role_permission_repo(self):
        return MagicMock()

    @pytest.fixture
    def permission_service(self, user_role_repo, role_permission_repo):
        return PermissionService(
            user_role_repo=user_role_repo,
            role_permission_repo=role_permission_repo,
        )

    def test_check_permission_returns_true_when_user_has_permission(
        self, permission_service, user_role_repo, role_permission_repo
    ):
        """Проверяет, что пользователь с ролью имеет требуемое разрешение."""
        user = MagicMock(pk=5)
        user_role_repo.get_role_ids_for_user.return_value = [1, 2]
        role_permission_repo.has_permission.return_value = True

        assert permission_service.check_permission(user, "edit_post") is True
        user_role_repo.get_role_ids_for_user.assert_called_once_with(5)
        role_permission_repo.has_permission.assert_called_once_with(
            [1, 2], "edit_post"
        )

    def test_check_permission_returns_false_when_no_roles(
        self, permission_service, user_role_repo, role_permission_repo
    ):
        """Проверяет, что без ролей разрешение не предоставляется."""
        user = MagicMock(pk=5)
        user_role_repo.get_role_ids_for_user.return_value = []

        assert permission_service.check_permission(user, "edit_post") is False
        user_role_repo.get_role_ids_for_user.assert_called_once_with(5)
        role_permission_repo.has_permission.assert_not_called()

    def test_check_permission_returns_false_when_permission_missing(
        self, permission_service, user_role_repo, role_permission_repo
    ):
        """Проверяет, что при отсутствии разрешения доступ запрещён."""
        user = MagicMock(pk=5)
        user_role_repo.get_role_ids_for_user.return_value = [3]
        role_permission_repo.has_permission.return_value = False

        assert (
            permission_service.check_permission(user, "delete_post") is False
        )
        role_permission_repo.has_permission.assert_called_once_with(
            [3], "delete_post"
        )

    def test_check_permission_returns_false_for_invalid_user(
        self, permission_service
    ):
        """
        Проверяет, что некорректный или отсутствующий пользователь
        не имеет доступа.
        """
        assert permission_service.check_permission(None, "view") is False
        assert (
            permission_service.check_permission(MagicMock(pk=None), "view")
            is False
        )
