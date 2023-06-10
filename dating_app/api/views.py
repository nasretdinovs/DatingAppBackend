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
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['gender', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name']


class UserMatchView(generics.CreateAPIView):
    queryset = User.objects.all()

    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
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
