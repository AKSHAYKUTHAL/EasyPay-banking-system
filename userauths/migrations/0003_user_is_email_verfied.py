# Generated by Django 4.2.5 on 2023-10-25 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0002_user_is_2fa'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_verfied',
            field=models.BooleanField(default=False),
        ),
    ]
