# Generated by Django 4.0.2 on 2022-03-07 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_issue_project_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='issue_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='issue_comments', to='api.issue'),
        ),
    ]