# Generated by Django 4.2 on 2023-05-06 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_alter_department_organisation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobtitle',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobtitles', to='organization.department'),
        ),
    ]