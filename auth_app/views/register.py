from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.serializers import RegisterSerializer
from core.container import get_auth_service


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = get_auth_service()
        try:
            user = auth_service.register_user(serializer.validated_data)
        except ValueError as exc:
            raise ValidationError(str(exc))

        output_serializer = RegisterSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
