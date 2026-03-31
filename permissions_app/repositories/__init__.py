"""Data access layer for permissions."""

from .permission import PermissionRepository
from .role import RoleRepository
from .user_role import UserRoleRepository
from .role_permission import RolePermissionRepository

__all__ = [
    "RoleRepository",
    "PermissionRepository",
    "UserRoleRepository",
    "RolePermissionRepository",
]
