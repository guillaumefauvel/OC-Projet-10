# Generated by Django 4.0.2 on 2022-03-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_comment_auth_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributors',
            name='permission',
            field=models.CharField(choices=[('Moderator', 'Moderator'), ('Contributor', 'Contributor')], max_length=32),
        ),
    ]
