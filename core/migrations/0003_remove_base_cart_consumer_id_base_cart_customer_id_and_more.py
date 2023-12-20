# Generated by Django 4.2.3 on 2023-08-11 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_base_items_item_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='base_cart',
            name='consumer_id',
        ),
        migrations.AddField(
            model_name='base_cart',
            name='customer_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='cust_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='base_cart',
            name='supplier_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supp_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Base_Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('qty', models.IntegerField()),
                ('price', models.FloatField()),
                ('discount', models.FloatField()),
                ('date', models.DateTimeField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Customer_id', to=settings.AUTH_USER_MODEL)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.base_items')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Supplier_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
