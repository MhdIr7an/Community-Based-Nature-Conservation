# Generated by Django 4.2.3 on 2023-09-09 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_base_user_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base_user',
            name='pincode',
            field=models.CharField(default='', max_length=6),
        ),
    ]
