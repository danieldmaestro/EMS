# Generated by Django 4.2 on 2023-05-06 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_alter_jobtitle_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtitle',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_titles', to='organization.organization'),
        ),
    ]
