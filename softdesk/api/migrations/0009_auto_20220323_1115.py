# Generated by Django 3.2.12 on 2022-03-23 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20220323_1113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'get_latest_by': ['created_time']},
        ),
        migrations.AlterModelOptions(
            name='issue',
            options={'get_latest_by': ['created_time']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'get_latest_by': ['created_time']},
        ),
    ]
