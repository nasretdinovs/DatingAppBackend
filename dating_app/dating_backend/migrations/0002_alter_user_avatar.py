# Generated by Django 4.2.2 on 2023-06-14 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(upload_to='avatars/'),
        ),
    ]
