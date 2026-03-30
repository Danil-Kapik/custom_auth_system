from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.serializers import LoginSerializer
from core.container import get_auth_service


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = get_auth_service()
        try:
            session = auth_service.login(serializer.validated_data)
        except ValueError as exc:
            raise ValidationError(str(exc))

        return Response({"token": session.token}, status=status.HTTP_200_OK)
