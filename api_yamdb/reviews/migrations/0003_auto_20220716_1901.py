# Generated by Django 2.2.16 on 2022-07-16 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_myownuser_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myownuser',
            name='confirmation_code',
            field=models.CharField(max_length=60),
        ),
    ]
