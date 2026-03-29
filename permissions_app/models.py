from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "permissions_role"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Permission(models.Model):
    code = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "permissions_permission"
        ordering = ["code"]

    def __str__(self):
        return self.code


class UserRole(models.Model):
    user = models.ForeignKey(
        "auth_app.User",
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "permissions_user_role"
        unique_together = (("user", "role"),)

    def __str__(self):
        return f"{self.user_id}:{self.role.name}"


class RolePermission(models.Model):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="role_permissions",
    )
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "permissions_role_permission"
        unique_together = (("role", "permission"),)

    def __str__(self):
        return f"{self.role.name}:{self.permission.code}"
