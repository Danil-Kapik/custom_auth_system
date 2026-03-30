"""API views for auth."""

from auth_app.views.login import LoginView
from auth_app.views.register import RegisterView

__all__ = ["RegisterView", "LoginView"]
