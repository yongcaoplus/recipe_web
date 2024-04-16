# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 1:57 PM
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import json
import mysql.connector
import numpy as np
import os
from collections import defaultdict

def read_jsonl(filename):
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for item in lines:
            data.append(json.loads(item))
    return data

def write_to_mysql(index_dir, image_dir):
    all_data = []
    for file_name in os.listdir(index_dir):
        file_path = os.path.join(index_dir, file_name)
        data = read_jsonl(file_path)
        all_data.extend(data)
    print("all data len: ", len(all_data))
    # 建立与MySQL数据库的连接
    cnx = mysql.connector.connect(host="localhost", user="root", password="dc75c84d3b18dbd0", database="recipe", charset='utf8mb4')
    cursor = cnx.cursor()
    empty_count = 0
    saved_count = 0
    for i, data in enumerate(all_data):
        # breakpoint()
        if data['language'] == 'zh':
            empty_count += 1
            continue
        try:
            # 插入数据到Recipes表
            data['img_path'] = os.path.join('marvl', data['language'], data['left_img'])
            data['img_name'] = data['left_img']
            language = data['language']
            evaluated_times = 0
            ## clean output
            insert_query = "INSERT INTO myapp_allmarvldata (img_path, img_name, language, evaluated_times) " \
                        "VALUES (%s, %s, %s, %s)"
            values = (data['img_path'], data['img_name'], language, evaluated_times)
            cursor.execute(insert_query, values)
            saved_count += 1
        except Exception as e:
            print("error: ", e)
            breakpoint()
        cnx.commit()
    # 关闭数据库连接
    cursor.close()
    cnx.close()
    print("empty count: ", empty_count)
    print("saved count: ", saved_count)
    print("total: ", empty_count + saved_count)


# def write_to_mysql(index_dir, image_dir):
#     all_data = []
#     for file_name in os.listdir(index_dir):
#         file_path = os.path.join(index_dir, file_name)
#         data = read_jsonl(file_path)
#         all_data.extend(data)
#     langauge_num = defaultdict(int)
#     for data in all_data:
#         langauge_num[data['language']] += 1
#     print("langauge_num: ", langauge_num)
    

# # antonia 
# write_to_mysql("gpt4_task_2", "static/marvl_acl2024")
# acl 2024 gpt4_probing
write_to_mysql("gpt4_task_2", "static/marvl_acl2024")