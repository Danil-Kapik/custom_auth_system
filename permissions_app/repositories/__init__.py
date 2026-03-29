"""Data access layer for permissions."""

from .permission import PermissionRepository
from .role import RoleRepository

__all__ = ["RoleRepository", "PermissionRepository"]
