from api.serializers import UserCreateSerializer, UserSerializer
from dating_backend.models import LikedUsers, User
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
