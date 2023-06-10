from dating_backend.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .validators import validate_latitude, validate_longitude


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    Поля:
    - password: Пароль пользователя (только запись).
    """

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
            'email',
            'latitude',
            'longitude'
            ]

    def create(self, validated_data):
        """
        Создает нового пользователя.
        Аргументы:
        - validated_data: Проверенные данные пользователя.
        Возвращает:
        - user: Созданный пользователь.
        Вызывает:
        - None
        """
        user = User.objects.create_user(**validated_data)
        user.process_avatar()
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователя.
    Поля:
    - password: Пароль пользователя (только запись).
    - avatar: Аватар пользователя (обязательное поле).
    - latitude: Широта пользователя (с проверкой допустимого значения).
    - longitude: Долгота пользователя (с проверкой допустимого значения).
    """

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
        )
    avatar = serializers.ImageField(required=True)
    latitude = serializers.FloatField(validators=[validate_latitude])
    longitude = serializers.FloatField(validators=[validate_longitude])

    class Meta:
        model = User
        fields = [
            'avatar',
            'first_name',
            'last_name',
            'gender',
            'email',
            'username',
            'password',
            'latitude',
            'longitude'
        ]

    def create(self, validated_data):
        """
        Создает нового пользователя.
        Аргументы:
        - validated_data: Проверенные данные пользователя.
        Возвращает:
        - user: Созданный пользователь.
        Вызывает:
        - None
        """
        user = User.objects.create_user(**validated_data)
        user.process_avatar()
        return user
