# Generated by Django 4.2 on 2023-05-10 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0007_alter_staff_work_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='work_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
