# -*- coding: utf-8 -*-
# @Time    : 2023/5/22 3:42 PM 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import json
# reformat jsonl file as asciii file
import os

from fileinput import filename


def format_jaonl(file_path, dst_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            data.append(json.loads(line))
    with open(dst_path, 'w') as f:
        for line in data:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')

# format_jaonl("data/en2cn_sampled_gold_test.jsonl", "data/format_en2cn_sampled_gold_test.json")
# format_jaonl("data/cn2en_sampled_gold_test.jsonl", "data/format_cn2en_sampled_gold_test.json")

for filename in os.listdir(os.path.join("data", "results_cn2en")):
    format_jaonl(os.path.join("data", "results_cn2en", filename), os.path.join("data", "format_results_cn2en", filename))

for filename in os.listdir(os.path.join("data", "results_en2cn")):
    format_jaonl(os.path.join("data", "results_en2cn", filename), os.path.join("data", "format_results_en2cn", filename))