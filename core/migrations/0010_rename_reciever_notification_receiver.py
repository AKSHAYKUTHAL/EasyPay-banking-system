# Generated by Django 4.2.5 on 2023-10-19 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_notification_reciever_notification_sender_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='reciever',
            new_name='receiver',
        ),
    ]