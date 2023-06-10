from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserCreateView, UserListView, UserMatchView

app_name = 'api'


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('clients/create/', UserCreateView.as_view(), name='create-user'),
    path(
        'clients/<int:pk>/match/',
        UserMatchView.as_view(),
        name='match-user'
        ),
    path('list/', UserListView.as_view(), name='user-list'),
]
