# Generated by Django 4.2 on 2023-05-08 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0005_alter_staff_user_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='staff',
            new_name='staff_profile',
        ),
    ]
