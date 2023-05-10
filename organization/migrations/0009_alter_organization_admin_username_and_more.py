# Generated by Django 4.2 on 2023-05-09 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_alter_csvfile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='admin_username',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='company_email_domain',
            field=models.CharField(max_length=30, null=True),
        ),
    ]