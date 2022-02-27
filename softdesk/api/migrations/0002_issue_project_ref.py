# Generated by Django 4.0.2 on 2022-02-27 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='project_ref',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issues_project', to='api.project'),
        ),
    ]
