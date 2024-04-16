# Generated by Django 3.2.19 on 2023-06-06 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_auto_20230530_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComprehensionCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=255)),
                ('submit_time', models.IntegerField(default=0)),
                ('correct', models.IntegerField(default=0)),
            ],
        ),
    ]
