# Generated by Django 3.2.19 on 2023-05-22 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20230521_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeadaptation',
            name='user_email',
        ),
        migrations.RemoveField(
            model_name='recipeevaluation',
            name='user_email',
        ),
    ]
