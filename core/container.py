from auth_app.models import User, Session
from auth_app.repositories import UserRepository, SessionRepository
from permissions_app.models import Role, Permission
from permissions_app.repositories import RoleRepository, PermissionRepository


def get_user_repository():
    return UserRepository(User)


def get_session_repository():
    return SessionRepository(Session)


def get_role_repository():
    return RoleRepository(Role)


def get_permission_repository():
    return PermissionRepository(Permission)
