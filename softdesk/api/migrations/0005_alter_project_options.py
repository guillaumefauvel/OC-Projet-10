# Generated by Django 4.0.2 on 2022-03-16 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_contributors_permission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'get_latest_by': ['id']},
        ),
    ]
