# Generated by Django 4.2.3 on 2023-08-11 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_base_order_is_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='base_order',
            name='is_approved',
        ),
        migrations.DeleteModel(
            name='Base_Cart',
        ),
    ]
