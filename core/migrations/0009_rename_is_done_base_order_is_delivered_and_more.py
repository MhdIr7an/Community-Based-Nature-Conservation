# Generated by Django 4.2.3 on 2023-08-12 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_base_discussios'),
    ]

    operations = [
        migrations.RenameField(
            model_name='base_order',
            old_name='is_done',
            new_name='is_delivered',
        ),
        migrations.AddField(
            model_name='base_issue',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
