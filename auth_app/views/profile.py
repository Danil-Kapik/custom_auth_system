from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_app.serializers import ProfileSerializer, UpdateProfileSerializer
from core.container import get_auth_service


class ProfileView(APIView):
    def patch(self, request):
        if not getattr(request, "user", None):
            raise ValidationError(
                "Authentication credentials were not provided."
            )

        serializer = UpdateProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = get_auth_service()
        try:
            user = auth_service.update_profile(
                request.user, serializer.validated_data
            )
        except ValueError as exc:
            raise ValidationError(str(exc))

        output_serializer = ProfileSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        if not getattr(request, "user", None):
            raise ValidationError(
                "Authentication credentials were not provided."
            )

        auth_service = get_auth_service()
        try:
            auth_service.soft_delete_user(request.user)
        except ValueError as exc:
            raise ValidationError(str(exc))

        return Response(status=status.HTTP_204_NO_CONTENT)
