from api.serializers import UserCreateSerializer, UserSerializer
from dating_backend.models import LikedUsers, User
from django.conf import settings
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserCreateView(generics.CreateAPIView):
    """
    Создание нового пользователя.
    Предоставляет эндпоинт для создания нового пользователя.
    Методы:
    - post: Создает нового пользователя на основе предоставленных данных.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserListView(generics.ListAPIView):
    """
    Просмотр списка пользователей.
    Предоставляет эндпоинт для получения списка пользователей с возможностью
    фильтрации и поиска по различным полям.
    Поля:
    - serializer_class: Сериализатор, используемый для представления польз-лей.
    - filter_backends: Список классов фильтрации, опред-х методы фильтрации.
    - filterset_fields: Поля, по которым можно фильтровать список польз-лей.
    - search_fields: Поля, по которым можно выполнять поиск пользователей.
    Методы:
    - get_queryset: Возвращает queryset пользователей, подходящих под фильтры.
    """
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

    def get_queryset(self):
        # Получение значения параметра distance из запроса
        distance = self.request.query_params.get('distance', None)

        if distance:
            # Делим на 100, чтобы при поиске указывать расстояние в км
            distance = float(distance) / 100

            user_latitude = self.request.user.latitude
            user_longitude = self.request.user.longitude
            min_latitude = user_latitude - distance
            max_latitude = user_latitude + distance
            min_longitude = user_longitude - distance
            max_longitude = user_longitude + distance

            # Фильтрация участников в пределах заданной дистанции
            queryset = User.objects.filter(
                latitude__range=(min_latitude, max_latitude),
                longitude__range=(min_longitude, max_longitude)
            )
        else:
            queryset = User.objects.all()

        return queryset


class UserMatchView(generics.CreateAPIView):
    queryset = User.objects.all()

    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        """
        Создание взаимной симпатии между пользователями.
        Предоставляет эндпоинт для создания взаимной симпатии между текущим
        пользователем и целевым пользователем с заданным идентификатором.
        Аргументы:
        - request: Запрос, содержащий информацию о текущем пользователе.
        - pk: Идентификатор целевого пользователя.
        Возвращает:
        - HTTP_200_OK, если симпатия взаимная и отправлено уведомление об этом
        обоим пользователям.
        - HTTP_204_NO_CONTENT, если симпатия односторонняя или пользователь
        уже лайкнут.
        - HTTP_400_BAD_REQUEST, если текущий пользователь и целевой
        пользователь совпадают.
        - HTTP_404_NOT_FOUND, если целевой пользователь не найден.
        """
        try:
            current_user = request.user
            target_user = User.objects.get(id=pk)

            if current_user == target_user:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if LikedUsers.objects.filter(
                from_user=target_user,
                to_user=current_user
                    ).exists():
                return Response(status=status.HTTP_204_NO_CONTENT)

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
                print('Письмо ушло 1!')
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
                print('Письмо ушло 2!')
                send_mail(
                    'Взаимная симпатия',
                    target_user_message,
                    settings.EMAIL_HOST_USER,
                    [target_user_email]
                )

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
