from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.container import get_auth_service


class LogoutView(APIView):
    def post(self, request):
        token = self._extract_token(request)
        if not token:
            raise ValidationError("Authorization header is required.")

        auth_service = get_auth_service()
        try:
            auth_service.logout(token)
        except ValueError as exc:
            raise ValidationError(str(exc))

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _extract_token(self, request):
        authorization = request.META.get("HTTP_AUTHORIZATION", "")
        if isinstance(authorization, str) and authorization.startswith(
            "Bearer "
        ):
            return authorization.split(" ", 1)[1].strip()
        return None
