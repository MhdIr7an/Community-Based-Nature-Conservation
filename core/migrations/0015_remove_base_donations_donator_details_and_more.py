# Generated by Django 4.2.3 on 2023-09-09 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_base_user_pincode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='base_donations',
            name='donator_details',
        ),
        migrations.DeleteModel(
            name='Base_DonatorDetails',
        ),
    ]