# Generated by Django 5.0.6 on 2024-08-03 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_rename_category_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
