# Generated by Django 4.2.2 on 2023-06-09 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dating_backend', '0007_alter_user_liked_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='liked_users',
        ),
    ]