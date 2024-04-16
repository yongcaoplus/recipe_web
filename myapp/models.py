from django.db import models


# Create your models here.
class User(models.Model):
    user_email = models.CharField(max_length=255)


class RecipeAdaptation(models.Model):
    direction = models.CharField(max_length=100)
    source_id = models.CharField(max_length=50)
    source_title = models.CharField(max_length=100, null=True)
    source_title_translated = models.CharField(max_length=100, null=True)
    source_ingredients = models.CharField(max_length=1024)
    source_steps = models.CharField(max_length=2048)
    source_dish = models.CharField(max_length=50, null=True)
    source_index = models.IntegerField()
    ref_id = models.CharField(max_length=50)
    ref_title = models.CharField(max_length=100, null=True)
    ref_title_translated = models.CharField(max_length=100, null=True)
    ref_ingredients = models.CharField(max_length=1024)
    ref_steps = models.CharField(max_length=2048)
    ref_dish = models.CharField(max_length=100, null=True)
    labeled_times = models.IntegerField(default=0)
    source_steps_translated = models.CharField(max_length=2048)
    source_ingredients_translated = models.CharField(max_length=1024)


class AdaptationResults(models.Model):
    user_email = models.CharField(max_length=255)
    direction = models.CharField(max_length=100)
    source_id = models.CharField(max_length=50)
    adapted_title = models.CharField(max_length=100, null=True)
    adapted_ingredients = models.CharField(max_length=1024, null=True)
    adapted_steps = models.CharField(max_length=2048, null=True)
    comment = models.CharField(max_length=2048, null=True)
    submission_time = models.DateTimeField(auto_now_add=True)  # 添加表格提交时间字段
    adaptation_time = models.IntegerField(null=True)  # 添加评估所用时间字段


class RecipeEvaluation(models.Model):
    direction = models.CharField(max_length=50)
    source_id = models.CharField(max_length=50)
    source_title = models.CharField(max_length=100, null=True)
    source_ingredients = models.CharField(max_length=1024, null=True)
    source_steps = models.CharField(max_length=2048, null=True)
    ref_recipe = models.CharField(max_length=3096, null=True)
    generated_recipe = models.CharField(max_length=3096)
    methods = models.CharField(max_length=100)
    evaluated_times = models.IntegerField(default=0)


class EvaluationResults(models.Model):
    user_email = models.CharField(max_length=255)
    direction = models.CharField(max_length=50)
    source_id = models.CharField(max_length=50)
    generated_recipe = models.CharField(max_length=3096)
    method = models.CharField(max_length=100)
    grammar_score = models.PositiveSmallIntegerField(null=True)
    correct_score = models.PositiveSmallIntegerField(null=True)
    preservation_score = models.PositiveSmallIntegerField(null=True)
    cultural_align_score = models.PositiveSmallIntegerField(null=True)
    submission_time = models.DateTimeField(auto_now_add=True)  # 添加表格提交时间字段
    evaluation_time = models.IntegerField(null=True)  # 添加评估所用时间字段
    comment = models.CharField(max_length=1024, null=True)

class ComprehensionCheck(models.Model):
    user_email = models.CharField(max_length=255)
    submit_time = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)


class GPT4EvaluationSource(models.Model):
    image_id = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    left_img = models.CharField(max_length=512)
    right_img = models.CharField(max_length=512)
    golden = models.CharField(max_length=512)
    gpt4_ret = models.CharField(max_length=512)
    evaluated_times = models.IntegerField(default=0)


class GPT4EvaluationResults(models.Model):
    user_email = models.CharField(max_length=255)
    image_id = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    s4 = models.CharField(max_length=10)
    s1 = models.IntegerField(null=True)
    s2 = models.IntegerField(null=True)
    s3 = models.IntegerField(null=True)
    s5 = models.IntegerField(null=True)
    evaluation_time = models.IntegerField(null=True)  # 添加评估所用时间字段
    submission_time = models.DateTimeField(auto_now_add=True) 
    comment = models.CharField(max_length=1024, null=True)


class GPT4ComprehensionCheck(models.Model):
    user_email = models.CharField(max_length=255)
    submit_time = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)


class AllMaRVLData(models.Model):
    img_path = models.CharField(max_length=256)
    img_name = models.CharField(max_length=64)
    language = models.CharField(max_length=10)
    evaluated_times = models.IntegerField(default=0)

class FilterMaRVLResults(models.Model):
    user_email = models.CharField(max_length=255)
    img_path_1 = models.CharField(max_length=256)
    img_path_2 = models.CharField(max_length=256)
    img_path_3 = models.CharField(max_length=256)
    img_path_4 = models.CharField(max_length=256)
    img_path_5 = models.CharField(max_length=256)
    label_1 = models.IntegerField(null=True)
    label_2 = models.IntegerField(null=True)
    label_3 = models.IntegerField(null=True)
    label_4 = models.IntegerField(null=True)
    label_5 = models.IntegerField(null=True)
    language = models.CharField(max_length=10)
    evaluation_time = models.IntegerField(null=True)  # 添加评估所用时间字段
    submission_time = models.DateTimeField(auto_now_add=True) 