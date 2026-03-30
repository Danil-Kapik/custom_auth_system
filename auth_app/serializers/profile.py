from rest_framework import serializers

from auth_app.models import User


class ProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(max_length=User.NAME_MAX_LENGTH)
    first_name = serializers.CharField(
        max_length=User.NAME_MAX_LENGTH, allow_blank=True
    )
    last_name = serializers.CharField(
        max_length=User.NAME_MAX_LENGTH, allow_blank=True
    )


class UpdateProfileSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=User.NAME_MAX_LENGTH, required=False
    )
    first_name = serializers.CharField(
        max_length=User.NAME_MAX_LENGTH, required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        max_length=User.NAME_MAX_LENGTH, required=False, allow_blank=True
    )
