# Generated by Django 4.2.3 on 2023-08-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_discount_base_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='base_order',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]