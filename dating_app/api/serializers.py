from dating_backend.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
        )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'avatar',
            'first_name',
            'last_name',
            'gender',
            'email'
            ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.process_avatar()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
        )
    avatar = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'gender',
            'email',
            'username',
            'password'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.process_avatar()
        return user
