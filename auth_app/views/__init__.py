"""API views for auth."""

from auth_app.views.login import LoginView
from auth_app.views.logout import LogoutView
from auth_app.views.profile import ProfileView
from auth_app.views.register import RegisterView

__all__ = ["RegisterView", "LoginView", "LogoutView", "ProfileView"]
