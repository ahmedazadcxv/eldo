# Generated by Django 3.0.8 on 2020-08-18 11:37

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='users/avatar.jpg', upload_to=accounts.models.user_directory_path),
        ),
    ]