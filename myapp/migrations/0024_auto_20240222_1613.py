# Generated by Django 3.2.19 on 2024-02-22 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_auto_20240222_1529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filtermarvlresults',
            old_name='img_path_label_1',
            new_name='img_path_1',
        ),
        migrations.RenameField(
            model_name='filtermarvlresults',
            old_name='img_path_label_2',
            new_name='img_path_2',
        ),
        migrations.RenameField(
            model_name='filtermarvlresults',
            old_name='img_path_label_3',
            new_name='img_path_3',
        ),
        migrations.RenameField(
            model_name='filtermarvlresults',
            old_name='img_path_label_4',
            new_name='img_path_4',
        ),
        migrations.RenameField(
            model_name='filtermarvlresults',
            old_name='img_path_label_5',
            new_name='img_path_5',
        ),
        migrations.AddField(
            model_name='filtermarvlresults',
            name='label_1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='filtermarvlresults',
            name='label_2',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='filtermarvlresults',
            name='label_3',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='filtermarvlresults',
            name='label_4',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='filtermarvlresults',
            name='label_5',
            field=models.IntegerField(null=True),
        ),
    ]
