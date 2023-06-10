# Generated by Django 4.2.2 on 2023-06-09 17:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating_backend', '0008_remove_user_liked_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]