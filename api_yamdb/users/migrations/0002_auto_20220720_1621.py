# Generated by Django 2.2.16 on 2022-07-20 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_staff',
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.UniqueConstraint(fields=('username', 'email'), name='unique_users'),
        ),
    ]
