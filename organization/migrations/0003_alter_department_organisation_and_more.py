# Generated by Django 4.2 on 2023-05-06 10:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_alter_department_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='organization.organization'),
        ),
        migrations.AlterField(
            model_name='jobtitle',
            name='department',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobtitles', to='organization.department'),
        ),
    ]
