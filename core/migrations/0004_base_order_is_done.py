# Generated by Django 4.2.3 on 2023-08-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_base_cart_consumer_id_base_cart_customer_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='base_order',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]