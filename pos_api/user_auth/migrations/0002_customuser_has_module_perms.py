# Generated by Django 5.0.6 on 2024-08-19 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='has_module_perms',
            field=models.BooleanField(default=True),
        ),
    ]
