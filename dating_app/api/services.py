from api.serializers import UserSerializer
from dating_backend.models import LikedUsers, User
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status

from .utils import calculate_distance


class UserService:
    @staticmethod
    def create_user(data):
        """
        Создает нового пользователя на основе предоставленных данных.
        Аргументы:
        - data: Данные пользователя для создания.
        Возвращает:
        - Созданный пользователь.
        """
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return user

    @staticmethod
    def get_filtered_users(request):
        """
        Возвращает отфильтрованный список пользователей с учетом параметров.
        Аргументы:
        - request: Запрос, содержащий параметры фильтрации.
        Возвращает:
        - Отфильтрованный queryset пользователей.
        """
        distance = request.query_params.get('distance', None)

        if distance:
            distance = float(distance)

            user_latitude = request.user.latitude
            user_longitude = request.user.longitude

            queryset = User.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False
            )

            filtered_users = []
            for user in queryset:
                user_distance = calculate_distance(
                    user_latitude,
                    user_longitude,
                    user.latitude,
                    user.longitude
                )
                if user_distance <= distance:
                    filtered_users.append(user)

            return User.objects.filter(
                id__in=[user.id for user in filtered_users])
        else:
            queryset = User.objects.all()
            return queryset


class UserMatchService:
    @staticmethod
    def create_mutual_sympathy(current_user, target_user):
        """
        Создает взаимную симпатию между пользователями.
        Аргументы:
        - current_user: Текущий пользователь.
        - target_user: Целевой пользователь.
        Возвращает:
        - Код статуса HTTP в зависимости от результата операции.
        """
        if current_user == target_user:
            return status.HTTP_400_BAD_REQUEST

        if LikedUsers.objects.filter(
            from_user=target_user,
            to_user=current_user
        ).exists():
            return status.HTTP_204_NO_CONTENT

        LikedUsers.objects.create(
            from_user=target_user,
            to_user=current_user
        )

        if current_user.check_mutual_sympathy(target_user):
            current_user_email = current_user.email
            current_user_message = (
                f'Вы понравились {target_user.first_name}! '
                f'Почта участника: {target_user.email}'
            )
            send_mail(
                'Взаимная симпатия',
                current_user_message,
                settings.EMAIL_HOST_USER,
                [current_user_email]
            )

            target_user_email = target_user.email
            target_user_message = (
                f'Вы понравились {current_user.first_name}! '
                f'Почта участника: {current_user.email}'
            )
            send_mail(
                'Взаимная симпатия',
                target_user_message,
                settings.EMAIL_HOST_USER,
                [target_user_email]
            )

            return status.HTTP_200_OK
        else:
            return status.HTTP_204_NO_CONTENT
