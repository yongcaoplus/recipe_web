# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 6:19 PM 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import json
import mysql.connector
import numpy as np
import os
import csv

cnx = mysql.connector.connect(host="localhost", user="root", password="dc75c84d3b18dbd0", database="recipe", charset='utf8mb4')
cursor = cnx.cursor()


def find_and_save_results(save_name, direction, source_ids, methods_list):
    with open(save_name, "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["method"] + source_ids)
        all_rets = []
        for methods in methods_list:
            eval_num = []
            for source_id in source_ids:
                query = "select count(*) from myapp_evaluationresults where direction='{}' and source_id='{}' and method='{}'".format(
                    direction, source_id, methods)
                cursor.execute(query)
                results = cursor.fetchall()[0][0]
                eval_num.append(results)
            all_rets.extend(eval_num)
            eval_num.insert(0, methods)
            csvwriter.writerow(eval_num)
    # statis all 0 in all_rets
    print("{} unlabeled num: {}".format(direction, len([item for item in all_rets if item == 0])))

methods_list = ["bloom_adapted", "mt_finetuned", "gpt4", "mt_zeroshot", "mt5_base"]
query = "select distinct source_id  from myapp_recipeevaluation where direction='en2cn'"
cursor.execute(query)
en2cn_source_ids = [item[0] for item in cursor.fetchall()]
query = "select distinct source_id  from myapp_recipeevaluation where direction='cn2en'"
cursor.execute(query)
cn2en_source_ids = [item[0] for item in cursor.fetchall()]


find_and_save_results("en2cn_evaluation_statistics.csv", "en2cn", en2cn_source_ids, methods_list)
find_and_save_results("cn2en_evaluation_statistics.csv", "cn2en", cn2en_source_ids, methods_list)

# with open ("en2cn_source_ids.csv", "w") as f:
#     csvwriter = csv.writer(f)
#     for methods in methods_list:
#         eval_num = []
#         for source_id in en2cn_source_ids:
#             query = "select count(*) from myapp_evaluationresults where direction='en2cn' and source_id='{}' and method='{}'".format(source_id, methods)
#             cursor.execute(query)
#             results = cursor.fetchall()[0][0]
#             eval_num.append(results)
#         eval_num.insert(0, methods)
#         csvwriter.writerow(eval_num)