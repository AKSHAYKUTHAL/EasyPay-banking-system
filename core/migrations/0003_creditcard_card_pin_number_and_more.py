# Generated by Django 4.2.5 on 2023-10-17 04:59

from django.db import migrations, models
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_transaction_transaction_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='card_pin_number',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=4, max_length=4, prefix=''),
        ),
        migrations.AlterField(
            model_name='creditcard',
            name='card_type',
            field=models.CharField(choices=[('master', 'Master'), ('visa', 'Visa'), ('rupay', 'Rupay')], default='master', max_length=20),
        ),
    ]
