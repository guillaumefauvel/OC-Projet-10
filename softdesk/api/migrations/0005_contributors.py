# Generated by Django 4.0.2 on 2022-02-28 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_comment_comment_id_remove_project_project_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('project_id', models.IntegerField()),
                ('permission', models.CharField(choices=[('Author', 'Author'), ('Contributor', 'Contributor')], max_length=32)),
                ('role', models.CharField(max_length=32)),
            ],
        ),
    ]
