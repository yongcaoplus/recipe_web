from django.shortcuts import render
import logging

logging.getLogger().setLevel("INFO")
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# import json
from django.db.models import Min
from random import sample
from django.db.models import Sum, Count
from .models import User, GPT4ComprehensionCheck, GPT4EvaluationSource, GPT4EvaluationResults
from django.db.models import F
import re
from datetime import timedelta


# 中文 gpt4 evaluation
def gpt4_compre_sw_27(request):
    return render(request, 'gpt4_compre_sw_27.html')

def submit_compre_sw_27(request):
    if request.method == 'GET':
        username = request.GET.get('user_email')
        s1 = request.GET.get('question1')
        s2 = request.GET.get('question2')
        s3 = request.GET.get('question3')
        s4 = request.GET.get('question4')
        s5 = request.GET.get('question5')
        user_checks = GPT4ComprehensionCheck.objects.filter(user_email=username)
        if user_checks.exists():
            return redirect("/stop_evaluation/")
        if int(s1) >= 4 and int(s2) < 4 and int(s3) >=4 and int(s4) >=4 and int(s5) == 2:
            return redirect("/gpt4_evaluate_sw_27/?user_email={}".format(username))
        else:
            new_check = GPT4ComprehensionCheck(user_email=username, submit_time=1)
            new_check.save()
            return redirect("/stop_evaluation/")

def gpt4_evaluate_sw_27(request):
    min_evaluated_times = GPT4EvaluationSource.objects.filter(language='sw').aggregate(min_evaluated_times=Min('evaluated_times'))['min_evaluated_times']
    gpt4_cases = GPT4EvaluationSource.objects.filter(language='sw', evaluated_times=min_evaluated_times)
    sampled_case = sample(list(gpt4_cases), 1)[0]
    return render(request, 'gpt4_evaluate_sw_27.html', {'gpt4_case': sampled_case})

def submit_evaluation_sw_27(request):
    if request.method == 'GET':
        s1 = request.GET.get('question1')
        s2 = request.GET.get('question2')
        s3 = request.GET.get('question3')
        s4 = request.GET.get('question4')
        s5 = request.GET.get('question5')
        comments = request.GET.get('comments')
        username = request.GET.get('user_email')
        language = request.GET.get('language')
        image_id = request.GET.get('image_id')
        submission_time = request.GET.get('submission_time')
        evaluation_time = request.GET.get('evaluation_time')
        GPT4EvaluationResults.objects.create(
            user_email=username,
            image_id=image_id,
            language=language,
            s1 = s1,
            s2 = s2,
            s3 = s3,
            s4 = s4,
            s5 = s5,
            evaluation_time=evaluation_time,
            submission_time=submission_time,
            comment=comments
        )
        GPT4EvaluationSource.objects.filter(language='sw', image_id=image_id).update(
            evaluated_times=F('evaluated_times') + 1)
        labeled_times_sum = \
            GPT4EvaluationResults.objects.filter(language='sw', user_email=username).count()
        # logging.info("000000  "+str(labeled_times_sum))
        if labeled_times_sum >= 5:
            return render(request, 'thank_paticipants.html')
        else:
            return redirect("/gpt4_evaluate_sw_27/?user_email=%s" % username)

def gpt4_compre_sw_27(request):
    return render(request, 'gpt4_compre_sw_27.html')


def submit_compre_sw_27(request):
    if request.method == 'GET':
        username = request.GET.get('user_email')
        s1 = request.GET.get('question1')
        s2 = request.GET.get('question2')
        s3 = request.GET.get('question3')
        s4 = request.GET.get('question4')
        s5 = request.GET.get('question5')
        user_checks = GPT4ComprehensionCheck.objects.filter(user_email=username)
        if user_checks.exists():
            return redirect("/stop_evaluation/")
        if int(s1) >= 4 and int(s2) < 4 and int(s3) >=4 and int(s4) >=4 and int(s5) == 2:
            return redirect("/gpt4_evaluate_sw_27/?user_email={}".format(username))
        else:
            new_check = GPT4ComprehensionCheck(user_email=username, submit_time=1)
            new_check.save()
            return redirect("/stop_evaluation/")

def gpt4_evaluate_sw_27(request):
    min_evaluated_times = GPT4EvaluationSource.objects.filter(language='sw').aggregate(min_evaluated_times=Min('evaluated_times'))['min_evaluated_times']
    gpt4_cases = GPT4EvaluationSource.objects.filter(language='sw', evaluated_times=min_evaluated_times)
    sampled_case = sample(list(gpt4_cases), 1)[0]
    return render(request, 'gpt4_evaluate_sw_27.html', {'gpt4_case': sampled_case})

# def submit_evaluation_sw_27(request):
#     if request.method == 'GET':
#         s1 = request.GET.get('question1')
#         s2 = request.GET.get('question2')
#         s3 = request.GET.get('question3')
#         s4 = request.GET.get('question4')
#         s5 = request.GET.get('question5')
#         comments = request.GET.get('comments')
#         username = request.GET.get('user_email')
#         language = request.GET.get('language')
#         image_id = request.GET.get('image_id')
#         submission_time = request.GET.get('submission_time')
#         evaluation_time = request.GET.get('evaluation_time')
#         GPT4EvaluationResults.objects.create(
#             user_email=username,
#             image_id=image_id,
#             language=language,
#             s1 = s1,
#             s2 = s2,
#             s3 = s3,
#             s4 = s4,
#             s5 = s5,
#             evaluation_time=evaluation_time,
#             submission_time=submission_time,
#             comment=comments
#         )
#         GPT4EvaluationSource.objects.filter(language='sw', image_id=image_id).update(
#             evaluated_times=F('evaluated_times') + 1)
#         labeled_times_sum = \
#             GPT4EvaluationResults.objects.filter(language='sw', user_email=username).count()
#         # logging.info("000000  "+str(labeled_times_sum))
#         if labeled_times_sum >= 5:
#             return render(request, 'thank_paticipants.html')
#         else:
#             return redirect("/gpt4_evaluate_sw_27/?user_email=%s" % username)