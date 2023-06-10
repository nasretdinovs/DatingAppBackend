from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from PIL import Image


class User(AbstractUser):
    """
    Пользователь приложения.

    Поля:
    - avatar: Фотография пользователя.
    - first_name: Имя пользователя.
    - last_name: Фамилия пользователя.
    - gender: Пол пользователя.
    - email: Email пользователя.
    - groups: Группы, к которым принадлежит пользователь.
    - user_permissions: Права доступа пользователя.
    - latitude: Широта местоположения пользователя.
    - longitude: Долгота местоположения пользователя.
    """

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    avatar = models.ImageField(upload_to='static/avatars/')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='custom_user_set'
        )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_set'
        )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def process_avatar(self):
        """
        Обработка аватара пользователя.
        Функция открывает изображение аватара и добавляет на него водяной знак.
        Результат сохраняется в файле аватара.
        """
        image = Image.open(self.avatar)
        watermark = Image.open('static/img/watermark.png')
        watermark = watermark.resize((50, 50))
        avatar_width, avatar_height = image.size
        watermark_width, watermark_height = watermark.size
        watermark_position = (
            avatar_width - watermark_width - 10,
            avatar_height - watermark_height - 10
            )
        image.paste(watermark, watermark_position, watermark)
        image.save(self.avatar.path)

    def check_mutual_sympathy(self, other_user):
        """
        Проверка взаимной симпатии между текущим пользователем и другим.
        Функция проверяет, существует ли запись о взаимной симпатии между
        текущим пользователем и другим пользователем в модели LikedUsers.
        Аргументы:
        - other_user: Пользователь, с которым проверяется взаимная симпатия.
        Возвращает:
        True, если существует взаимная симпатия, иначе False.
        """
        return LikedUsers.objects.filter(
            from_user=self,
            to_user=other_user
        ).exists() and LikedUsers.objects.filter(
            from_user=other_user,
            to_user=self
        ).exists()


class LikedUsers(models.Model):
    """
    Модель для хранения информации о взаимной симпатии пользователей.
    Поля:
    - from_user: Пользователь, инициирующий симпатию.
    - to_user: Пользователь, к которому проявляют симпатию.
    Метаданные:
    - unique_together: Пара (from_user, to_user) должна быть уникальной.
    Методы:
    - __str__: Возвращает строковое представление объекта.
    """

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_users_sent')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_users_received')

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'
