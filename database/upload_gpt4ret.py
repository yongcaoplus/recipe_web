# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 1:57 PM
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import json
import mysql.connector
import numpy as np
import os


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
        if "result" not in data:
            empty_count += 1
            continue
        try:
            # 插入数据到Recipes表
            data['left_img'] = os.path.join('marvl', data['language'], data['left_img'])
            data['right_img'] = os.path.join('marvl', data['language'], data['right_img'])
            ## clean output
            data['result'] = data['result'].split(":")[-1].strip()
            insert_query = "INSERT INTO myapp_gpt4evaluationsource (image_id, language, left_img, right_img, golden, gpt4_ret, evaluated_times) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (i, data['language'], data['left_img'], data['right_img'], data['caption'], data['result'], 0)
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


write_to_mysql("gpt4_task_1", "static/marvl")
