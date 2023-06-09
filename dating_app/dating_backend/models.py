from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    avatar = models.ImageField(upload_to='avatars/')
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
