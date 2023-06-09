from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserCreateView, UserMatchView, UserViewSet

app_name = 'api'


router = DefaultRouter()
router.register(r'clients', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('clients/create/', UserCreateView.as_view(), name='create-user'),
    path(
        'clients/<int:pk>/match/',
        UserMatchView.as_view(),
        name='match-user'
        ),
]
