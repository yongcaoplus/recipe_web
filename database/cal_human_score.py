# -*- coding: utf-8 -*-
# @Time    : 2023/7/17 1:37 PM 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
from collections import defaultdict
import csv
from prettytable import PrettyTable
import numpy as np
from tqdm import tqdm


# read csv files
def read_csv(filename):
    all_data = []
    with open(filename, 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)
        for line in csvreader:
            all_data.append(line)
    return all_data


def print_scores(grammar_score, correct_score, preserv_score, culture_align_score):
    table = PrettyTable()
    keys = list(grammar_score.keys())
    print_scores = []
    print(keys)
    table.field_names = ['Model', 'Grammar', 'var1', 'Correct', 'var2',  'Preserv', 'var3',  'Culture Align', 'var4']
    for key in ['mt_zeroshot', 'mt_finetuned', 'mt5_base','bloom_adapted', 'chatglm2', 'gpt4',  'human', 'retrival']:
        table.add_row([key, np.mean(grammar_score[key]), np.std(grammar_score[key]),
                       np.mean(correct_score[key]), np.std(correct_score[key]),
                       np.mean(preserv_score[key]), np.std(preserv_score[key]),
                       np.mean(culture_align_score[key]), np.std(culture_align_score[key])])
    table.float_format = ".2"
    print(table)


def get_scores(filename):
    data = read_csv(filename)
    grammar_score = defaultdict(list)
    correct_score = defaultdict(list)
    preserv_score = defaultdict(list)
    culture_align_score = defaultdict(list)
    recorded_id = defaultdict(int)
    # valid_ids = 0
    for item in (data):
        cur_id = item[1] + item[2]
        # if cur_id in recorded_id:
        #     continue
        # else:
        # recorded_id[cur_id] = int(item[7])
        grammar_score[item[2]].append(float(item[3]))
        correct_score[item[2]].append(float(item[4]))
        preserv_score[item[2]].append(float(item[5]))
        culture_align_score[item[2]].append(float(item[6]))
            # valid_ids += 1
    # print(valid_ids)
    print_scores(grammar_score, correct_score, preserv_score, culture_align_score)


print("-" * 20, "cn2en", "-" * 20)
get_scores('data/evaluation_results_cn2en_sep.csv')
print("-" * 20, "en2cn", "-" * 20)
get_scores('data/evaluation_results_en2cn_sep.csv')

