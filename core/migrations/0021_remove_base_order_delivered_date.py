# Generated by Django 4.2.3 on 2023-09-17 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_base_order_delivered_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='base_order',
            name='delivered_date',
        ),
    ]