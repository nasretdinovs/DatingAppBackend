from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from PIL import Image


class User(AbstractUser):
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

    def process_avatar(self):
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
        return LikedUsers.objects.filter(
            from_user=self, to_user=other_user).exists() and \
               LikedUsers.objects.filter(
            from_user=other_user, to_user=self).exists()


class LikedUsers(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_users_sent')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liked_users_received')

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'
