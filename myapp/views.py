from django.shortcuts import render
from .models import User
import logging

logging.getLogger().setLevel("INFO")
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json
from django.db.models import Min
from random import sample
from django.db.models import Sum, Count
from .models import AdaptationResults, RecipeAdaptation, User, RecipeEvaluation, EvaluationResults, GPT4ComprehensionCheck, GPT4EvaluationSource, GPT4EvaluationResults, AllMaRVLData, FilterMaRVLResults
from django.db.models import F
import re
from datetime import timedelta

from .cn_process import gpt4_compre_cn_1996, submit_compre_cn_1996, \
        gpt4_evaluate_cn_1996, submit_evaluation_cn_1996, gpt4_compre_cn_1996, \
        submit_compre_cn_1996, gpt4_evaluate_cn_1996

from .id_process import gpt4_compre_id_01, submit_compre_id_01, \
        gpt4_evaluate_id_01, submit_evaluation_id_01, gpt4_compre_id_01, \
        submit_compre_id_01, gpt4_evaluate_id_01

from .sw_process import gpt4_compre_sw_27, submit_compre_sw_27, \
        gpt4_evaluate_sw_27, submit_evaluation_sw_27, gpt4_compre_sw_27, \
        submit_compre_sw_27, gpt4_evaluate_sw_27

from .ta_process import gpt4_compre_ta_20, submit_compre_ta_20, \
        gpt4_evaluate_ta_20, submit_evaluation_ta_20, gpt4_compre_ta_20, \
        submit_compre_ta_20, gpt4_evaluate_ta_20

from .tr_process import gpt4_compre_tr_23, submit_compre_tr_23, \
        gpt4_evaluate_tr_23, submit_evaluation_tr_23, gpt4_compre_tr_23, \
        submit_compre_tr_23, gpt4_evaluate_tr_23

def return_filter_page(request, language):
    min_evaluated_times = AllMaRVLData.objects.filter(language=language).aggregate(min_evaluated_times=Min('evaluated_times'))['min_evaluated_times']
    gpt4_cases = AllMaRVLData.objects.filter(language=language, evaluated_times=min_evaluated_times)
    if len(list(gpt4_cases)) < 5:
        all_cases = AllMaRVLData.objects.filter(language=language)
        sampled_case = list(gpt4_cases) + sample(list(all_cases), 5-len(list(gpt4_cases)))
    else:
        sampled_case = sample(list(gpt4_cases), 5)
    return render(request, 'gpt4_filter_{}.html'.format(language), {'gpt4_case': sampled_case})


def gpt4_filter_tr(request):
    return return_filter_page(request, 'tr')

def gpt4_filter_sw(request):
    return return_filter_page(request, 'sw')

def gpt4_filter_ta(request):
    return return_filter_page(request, 'ta')

def gpt4_filter_id(request):
    return return_filter_page(request, 'id')


def submit_filter(request):
    if request.method == 'GET':
        username = request.GET.get('user_email')
        print(username)
        s1 = request.GET.get('question1')
        s2 = request.GET.get('question2')
        s3 = request.GET.get('question3')
        s4 = request.GET.get('question4')
        s5 = request.GET.get('question5')
        img_path_1 = request.GET.get('img_path_1')
        img_path_2 = request.GET.get('img_path_2')
        img_path_3 = request.GET.get('img_path_3')
        img_path_4 = request.GET.get('img_path_4')
        img_path_5 = request.GET.get('img_path_5')
        language = request.GET.get('language')
        submission_time = request.GET.get('submission_time')
        evaluation_time = request.GET.get('evaluation_time')
        FilterMaRVLResults.objects.create(
            user_email=username,
            language=language,
            label_1 = s1,
            label_2 = s2,
            label_3 = s3,
            label_4 = s4,
            label_5 = s5,
            img_path_1 = img_path_1,
            img_path_2 = img_path_2,
            img_path_3 = img_path_3, 
            img_path_4 = img_path_4,
            img_path_5 = img_path_5,
            evaluation_time=evaluation_time,
            submission_time=submission_time
        )
        AllMaRVLData.objects.filter(language=language, img_path=img_path_1).update(
            evaluated_times=F('evaluated_times') + 1)
        AllMaRVLData.objects.filter(language=language, img_path=img_path_2).update(
            evaluated_times=F('evaluated_times') + 1)
        AllMaRVLData.objects.filter(language=language, img_path=img_path_3).update(
            evaluated_times=F('evaluated_times') + 1)
        AllMaRVLData.objects.filter(language=language, img_path=img_path_4).update(
            evaluated_times=F('evaluated_times') + 1)
        AllMaRVLData.objects.filter(language=language, img_path=img_path_5).update(
            evaluated_times=F('evaluated_times') + 1)
        labeled_times_sum = \
            FilterMaRVLResults.objects.filter(language=language, user_email=username).count()
        if labeled_times_sum >= 20:
            return render(request, 'thank_paticipants.html')
        else:
            return redirect("/gpt4_filter_{}?user_email={}".format(language, username))

def get_user_gpt4_filter_num(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        language = data.get('language')
        username = data.get('username')
        record_count = FilterMaRVLResults.objects.filter(user_email=username, language=language).count()
        # record_count = 0
        print(record_count)
        response_data = {
            'record_count': record_count*5,
        }
        logging.info(username)
        logging.info(record_count)
        return JsonResponse(response_data)


def tutorial_video(request):
    return render(request, 'tutorial_video.html')


def evaluate_tutorial(request):
    return render(request, 'evaluation_welcome.html')


# Create your views here.
def index(request):
    return render(request, 'index.html')


def adapt_example(request):
    return render(request, 'adapt_example.html')


def evaluate_example(request):
    return render(request, 'evaluate_example.html')


def adapt_en2cn(request):
    # 视图函数的逻辑代码
    # 查询labeled_times的最小值
    min_labeled_times = \
    RecipeAdaptation.objects.filter(direction='en2cn').aggregate(min_labeled_times=Min('labeled_times'))[
        'min_labeled_times']
    # 随机选择一个具有最小labeled_times的记录
    record = RecipeAdaptation.objects.filter(direction='en2cn').filter(labeled_times=min_labeled_times).order_by(
        '?').first()
    # 获取该记录的source_id
    source_id = record.source_id
    recipe = RecipeAdaptation.objects.filter(direction='en2cn').filter(source_id=source_id).first()
    recipe.source_ingredients = recipe.source_ingredients.split("\t\t")
    recipe.source_steps = recipe.source_steps.split("\t\t")
    recipe.ref_ingredients = recipe.ref_ingredients.split("\t\t")
    recipe.ref_steps = recipe.ref_steps.split("\t\t")
    recipe.source_ingredients_translated = recipe.source_ingredients_translated.split("\t\t")
    recipe.source_steps_translated = recipe.source_steps_translated.split("\t\t")
    return render(request, 'adapt_en2cn.html', {'recipe': recipe})


def adapt_en2cn_admin(request):
    logging.info("-"*30)
    source_id = request.GET.get('source_id')
    recipe = RecipeAdaptation.objects.filter(direction='en2cn').filter(source_id=source_id).first()
    recipe.source_ingredients = recipe.source_ingredients.split("\t\t")
    recipe.source_steps = recipe.source_steps.split("\t\t")
    recipe.ref_ingredients = recipe.ref_ingredients.split("\t\t")
    recipe.ref_steps = recipe.ref_steps.split("\t\t")
    recipe.source_ingredients_translated = recipe.source_ingredients_translated.split("\t\t")
    recipe.source_steps_translated = recipe.source_steps_translated.split("\t\t")
    return render(request, 'adapt_en2cn_admin.html', {'recipe': recipe})

def adapt_cn2en(request):
    # 视图函数的逻辑代码
    # 查询labeled_times的最小值
    min_labeled_times = \
    RecipeAdaptation.objects.filter(direction='cn2en').aggregate(min_labeled_times=Min('labeled_times'))[
        'min_labeled_times']
    # 随机选择一个具有最小labeled_times的记录
    record = RecipeAdaptation.objects.filter(direction='cn2en').filter(labeled_times=min_labeled_times).order_by(
        '?').first()
    # 获取该记录的source_id
    source_id = record.source_id
    recipe = RecipeAdaptation.objects.filter(direction='cn2en').filter(source_id=source_id).first()
    recipe.source_ingredients = recipe.source_ingredients.split("\t\t")
    recipe.source_steps = recipe.source_steps.split("\t\t")
    recipe.ref_ingredients = recipe.ref_ingredients.split("\t\t")
    recipe.ref_steps = recipe.ref_steps.split("\t\t")
    recipe.source_ingredients_translated = recipe.source_ingredients_translated.split("\t\t")
    recipe.source_steps_translated = recipe.source_steps_translated.split("\t\t")
    return render(request, 'adapt_cn2en.html', {'recipe': recipe})



def remove_comma(strings):
    return re.sub(r"^[,:，：]+\s*(.*)$", r"\1", strings).rstrip(",，").strip()


def format_recipe(content):
    title = None
    ingredients = None
    steps = None
    try:
        # 查找标题
        title_match = re.search(
            r"(标题|Tile|Title:|title:)\s*(.*?)\s*(ingredients:|Ingredients:|ingredient:|Ingredient:|Ingrids|Ingridents|原料|成分|$)",
            content, re.IGNORECASE)
        if title_match:
            title = title_match.group(2).strip()

        # 查找成分
        ingredient_match = re.search(
            r"\b(ingredients:|Ingrids|Ingredients:|ingredient:|Ingridents|Ingredient:|原料|成分)\s*(.*?)\s*\b(步骤|Steps:|steps:|step:|Step:|$)",
            content, re.IGNORECASE)
        if ingredient_match:
            ingredients = ingredient_match.group(2).strip()

        # 查找步骤
        step_match = re.search(r"\b(步骤|Steps:|steps:|step:|Step:)\s*(.*)", content, re.IGNORECASE)
        if step_match:
            steps = step_match.group(2).strip()
        result = [remove_comma(title), remove_comma(ingredients), remove_comma(steps)]
        if all(info is not None for info in result):
            return result
        else:
            return [content]
    except:
        return [content]


def evaluate_compre_cn2en(request):
    return render(request, 'evaluate_compre_cn2en.html')


def evaluate_compre_en2cn(request):
    return render(request, 'evaluate_compre_en2cn.html')


def evaluate_en2cn(request):
    # Retrieve the minimum evaluated_times for direction='en2cn' from RecipeEvaluation table
    min_evaluated_times = \
        RecipeEvaluation.objects.filter(direction='en2cn').aggregate(min_evaluated_times=Min('evaluated_times'))[
            'min_evaluated_times']
    recipes = RecipeEvaluation.objects.filter(direction='en2cn', evaluated_times=min_evaluated_times)
    sampled_recipe = sample(list(recipes), 1)[0]
    sampled_recipe.source_ingredients = sampled_recipe.source_ingredients.split("\t\t")
    sampled_recipe.source_steps = sampled_recipe.source_steps.split("\t\t")
    sampled_recipe.generated_recipe = format_recipe(sampled_recipe.generated_recipe)
    return render(request, 'evaluate_en2cn.html', {'recipe': sampled_recipe})


def evaluate_cn2en(request):
    # 视图函数的逻辑代码
    min_evaluated_times = \
        RecipeEvaluation.objects.filter(direction='cn2en').aggregate(min_evaluated_times=Min('evaluated_times'))[
            'min_evaluated_times']
    recipes = RecipeEvaluation.objects.filter(direction='cn2en', evaluated_times=min_evaluated_times)
    sampled_recipe = sample(list(recipes), 1)[0]
    sampled_recipe.source_ingredients = sampled_recipe.source_ingredients.split("\t\t")
    sampled_recipe.source_steps = sampled_recipe.source_steps.split("\t\t")
    sampled_recipe.generated_recipe = format_recipe(sampled_recipe.generated_recipe)
    return render(request, 'evaluate_cn2en.html', {'recipe': sampled_recipe})


def loginin(request):
    return render(request, 'loginin.html')


def logout(request):
    request.session['is_login'] = False
    request.session['user_id'] = None
    # 视图函数的逻辑代码
    return redirect("/")


def register(request):
    email = request.GET.get('email')
    print("======= ", email)
    # 视图函数的逻辑代码
    return render(request, 'register.html', {'email': email})


def contact(request):
    # 视图函数的逻辑代码
    return render(request, 'contact.html')


def get_user_progress(request):
    if request.method == 'POST':
        min_duty_expectations = 15
        data = json.loads(request.body)
        direction = data.get('direction')
        username = data.get('username')
        record_count = AdaptationResults.objects.filter(user_email=username, direction=direction).count()
        # 计算总标注量
        total_annotation_count = RecipeAdaptation.objects.filter(direction=direction).count() * 2
        # 计算已标注量
        labeled_times_sum = \
        RecipeAdaptation.objects.filter(direction=direction).aggregate(total_labeled_times=Sum('labeled_times'))[
            'total_labeled_times']
        # 计算用户数
        user_count = User.objects.count()
        logging.info('User count' + str(user_count))
        logging.info('labeled_times_sum ' + str(labeled_times_sum))
        logging.info('total_annotation_count ' + str(total_annotation_count))
        # 计算每个用户需要标注的数量
        annotations_per_user = (total_annotation_count - labeled_times_sum) // user_count
        response_data = {
            'record_count': record_count,
            'duty': min(annotations_per_user, min_duty_expectations)
        }
        logging.info(record_count)
        return JsonResponse(response_data)


def get_user_evaluation_num(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        direction = data.get('direction')
        username = data.get('username')
        record_count = EvaluationResults.objects.filter(user_email=username, direction=direction).count()
        response_data = {
            'record_count': record_count+1,
        }
        logging.info(username)
        logging.info(record_count)
        return JsonResponse(response_data)

def get_user_gpt4_evaluation_num(request):
    logging.info("get_user_gpt4_evaluation_num")
    if request.method == 'POST':
        data = json.loads(request.body)
        language = data.get('language')
        username = data.get('username')
        record_count = GPT4EvaluationResults.objects.filter(user_email=username, language=language).count()
        # record_count = 0
        response_data = {
            'record_count': record_count+1,
        }
        logging.info(username)
        logging.info(record_count)
        return JsonResponse(response_data)


def get_user_gpt4_progress(request):
    if request.method == 'POST':
        min_duty_expectations = 15
        data = json.loads(request.body)
        direction = data.get('direction')
        username = data.get('username')
        record_count = AdaptationResults.objects.filter(user_email=username, direction=direction).count()
        # 计算总标注量
        total_annotation_count = RecipeAdaptation.objects.filter(direction=direction).count() * 2
        # 计算已标注量
        labeled_times_sum = \
        RecipeAdaptation.objects.filter(direction=direction).aggregate(total_labeled_times=Sum('labeled_times'))[
            'total_labeled_times']
        # 计算用户数
        user_count = User.objects.count()
        logging.info('User count' + str(user_count))
        logging.info('labeled_times_sum ' + str(labeled_times_sum))
        logging.info('total_annotation_count ' + str(total_annotation_count))
        # 计算每个用户需要标注的数量
        annotations_per_user = (total_annotation_count - labeled_times_sum) // user_count
        response_data = {
            'record_count': record_count,
            'duty': min(annotations_per_user, min_duty_expectations)
        }
        logging.info(record_count)
        return JsonResponse(response_data)

def check_email(request):
    email = request.POST.get('email')
    data = {'exists': False}
    if email:
        try:
            user = User.objects.get(user_email=email)
            data['exists'] = True
            request.session['is_login'] = True
            request.session['user_id'] = email
            return JsonResponse(data)
        except User.DoesNotExist:
            pass
    return JsonResponse(data)


def submit_adapt(request):
    if request.method == 'POST':
        recipe_title = request.POST.get('adapted_title')
        recipe_ingredients = request.POST.get('adapted_ingredients')
        recipe_steps = request.POST.get('adapted_steps')
        comment = request.POST.get('adapted_comments')
        username = request.POST.get('user_email')
        direction = request.POST.get('direction')
        source_id = request.POST.get('source_id')
        submission_time = request.POST.get('submission_time')
        adaptation_time = request.POST.get('adaptation_time')
        adaptation_result = AdaptationResults.objects.create(
            source_id=source_id,
            adapted_title=recipe_title,
            adapted_ingredients=recipe_ingredients,
            adapted_steps=recipe_steps,
            comment=comment,
            user_email=username,
            submission_time=submission_time,
            adaptation_time=adaptation_time,
            direction=direction
        )
        RecipeAdaptation.objects.filter(direction=direction, source_id=source_id).update(
            labeled_times=F('labeled_times') + 1)

    if direction == "cn2en":
        return redirect("/adapt_cn2en/")
    else:
        return redirect("/adapt_en2cn/")


def submit_adapt_admin(request):
    if request.method == 'POST':
        recipe_title = request.POST.get('adapted_title')
        recipe_ingredients = request.POST.get('adapted_ingredients')
        recipe_steps = request.POST.get('adapted_steps')
        comment = request.POST.get('adapted_comments')
        username = request.POST.get('user_email')
        direction = request.POST.get('direction')
        source_id = request.POST.get('source_id')
        submission_time = request.POST.get('submission_time')
        adaptation_time = request.POST.get('adaptation_time')
        adaptation_result = AdaptationResults.objects.create(
            source_id=source_id,
            adapted_title=recipe_title,
            adapted_ingredients=recipe_ingredients,
            adapted_steps=recipe_steps,
            comment=comment,
            user_email=username,
            submission_time=submission_time,
            adaptation_time=adaptation_time,
            direction=direction
        )
        RecipeAdaptation.objects.filter(direction=direction, source_id=source_id).update(
            labeled_times=F('labeled_times') + 1)

    if direction == "cn2en":
        return redirect("/adapt_cn2en_admin/?source_id=")
    else:
        return redirect("/adapt_en2cn_admin/?source_id=")

def submit_evaluation(request):
    if request.method == 'GET':
        grammer = request.GET.get('question1')
        correctness = request.GET.get('question2')
        preservation = request.GET.get('question3')
        cultural_appropriateness = request.GET.get('question4')
        comments = request.GET.get('comments')
        username = request.GET.get('user_email')
        direction = request.GET.get('direction')
        source_id = request.GET.get('source_id')
        generated_recipe = request.GET.get('generated_recipe')
        methods = request.GET.get('methods')
        submission_time = request.GET.get('submission_time')
        evaluation_time = request.GET.get('evaluation_time')
        EvaluationResults.objects.create(
            user_email=username,
            direction=direction,
            source_id=source_id,
            generated_recipe=generated_recipe,
            method=methods,
            grammar_score=grammer,
            correct_score=correctness,
            preservation_score=preservation,
            cultural_align_score=cultural_appropriateness,
            evaluation_time=evaluation_time,
            submission_time=submission_time,
            comment=comments
        )
        RecipeEvaluation.objects.filter(direction=direction, source_id=source_id, methods=methods).update(
            evaluated_times=F('evaluated_times') + 1)
        labeled_times_sum = \
            EvaluationResults.objects.filter(direction=direction, user_email=username).count()
        logging.info("000000  "+str(labeled_times_sum))
        if labeled_times_sum >= 3:
            return render(request, 'thank_paticipants.html')
        else:
            if direction == "en2cn":
                return redirect("/evaluate_en2cn/?user_email=%s" % username)
            else:
                return redirect("/evaluate_cn2en/?user_email=%s" % username)



def submit_comprehension(request):
    if request.method == 'GET':
        username = request.GET.get('user_email')
        grammer = request.GET.get('question1')
        correctness = request.GET.get('question2')
        cultural_appropriateness = request.GET.get('question4')
        direction = request.GET.get('direction')
        user_checks = ComprehensionCheck.objects.filter(user_email=username)
        if user_checks.exists():
            if user_checks.values_list('submit_time', flat=True).first() > 1:
                return redirect("/stop_evaluation/")
        if int(grammer) <= 2 and int(correctness) <= 2 and int(cultural_appropriateness) <= 3:
            if direction == "en2cn":
                return redirect("/evaluate_en2cn/?user_email={}".format(username))
            else:
                return redirect("/evaluate_cn2en/?user_email={}".format(username))
        else:
            user_checks = ComprehensionCheck.objects.filter(user_email=username)
            logging.info(user_checks)
            if not user_checks.exists():
                new_check = ComprehensionCheck(user_email=username, submit_time=1)
                new_check.save()
                if direction == "en2cn":
                    return redirect("/evaluate_compre_en2cn/?user_email={}&left_time={}".format(username, 2))
                else:
                    return redirect("/evaluate_compre_cn2en/?user_email={}&left_time={}".format(username, 2))
            else:
                ComprehensionCheck.objects.filter(user_email=username).update(
                    submit_time=F('submit_time') + 1)
                return redirect("/stop_evaluation/")


def stop_evaluation(request):
    return render(request, 'stop_evaluation.html')


def register_user(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        email = body.get('email')
        # 检查用户是否已存在
        if User.objects.filter(user_email=email).exists():
            request.session['is_login'] = True
            request.session['user_id'] = email
            # 用户已存在，弹出提示框并重定向到登录页面
            return JsonResponse({"data": 0})
        # 用户不存在，创建新用户
        user = User.objects.create(user_email=email)
        request.session['is_login'] = True
        request.session['user_id'] = email
        # 其他操作...
        return JsonResponse({"data": 1})
    else:
        return JsonResponse({"data": 2})
