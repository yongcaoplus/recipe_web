# Generated by Django 3.2.19 on 2023-05-22 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20230522_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adaptationresults',
            name='adapted_ingredients',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationresults',
            name='adapted_steps',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationresults',
            name='adapted_title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationresults',
            name='comment',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='adaptationresults',
            name='direction',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='adaptationresults',
            name='source_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='evaluationresults',
            name='comment',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='evaluationresults',
            name='direction',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='evaluationresults',
            name='generated_recipe',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='evaluationresults',
            name='method',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='evaluationresults',
            name='source_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='direction',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='ref_dish',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='ref_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='ref_ingredients',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='ref_steps',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='ref_title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='ref_title_translated',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='source_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='source_ingredients',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='source_steps',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='source_title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipeadaptation',
            name='source_title_translated',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='direction',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='generated_recipe',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='method',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='source_dish',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='source_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='source_index',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='source_ingredients',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='source_steps',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='source_title',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='recipeevaluation',
            name='source_title_translated',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
