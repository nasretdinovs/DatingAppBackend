# Generated by Django 4.2.2 on 2023-06-10 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating_backend', '0010_remove_user_liked_users_likedusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]