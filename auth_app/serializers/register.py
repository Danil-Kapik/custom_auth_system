from rest_framework import serializers

from auth_app.models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=User.EMAIL_MAX_LENGTH)
    username = serializers.CharField(max_length=User.NAME_MAX_LENGTH)
    first_name = serializers.CharField(
        max_length=User.NAME_MAX_LENGTH, required=False, allow_blank=True
    )
    last_name = serializers.CharField(
        max_length=User.NAME_MAX_LENGTH, required=False, allow_blank=True
    )
    password = serializers.CharField(max_length=128, write_only=True)
