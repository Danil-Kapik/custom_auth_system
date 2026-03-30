from auth_app.models import User, Session
from auth_app.repositories import UserRepository, SessionRepository
from auth_app.services import AuthService
from permissions_app.models import Role, Permission
from permissions_app.repositories import RoleRepository, PermissionRepository


def get_user_repository():
    return UserRepository(User)


def get_session_repository():
    return SessionRepository(Session)


def get_auth_service():
    return AuthService(user_repository=get_user_repository())


def get_role_repository():
    return RoleRepository(Role)


def get_permission_repository():
    return PermissionRepository(Permission)
