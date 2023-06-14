from api.serializers import UserCreateSerializer, UserSerializer
from api.services import UserMatchService, UserService
from dating_backend.models import User
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
        queryset = UserService.get_filtered_users(self.request)
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

            response_status = UserMatchService.create_mutual_sympathy(
                current_user,
                target_user
            )
            return Response(status=response_status)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
