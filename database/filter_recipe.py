# -*- coding: utf-8 -*-
# @Time    : 2023/5/27 12:29 AM 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import json


def process_jsonl_file(file_path):
    invalid_ids = []
    # 读取JSONL文件
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            # 解析JSON数据
            data = json.loads(line)

            # 打印数据
            print("progress:", i+1)
            print("Title:", data['source']["title"])
            print("Ingredients:", data['source']["ingredients"])
            print("Steps:", data['source']["steps"])
            print()

            # 获取用户输入
            user_input = input("按回车保留该数据，输入1表示不合格：")

            # 根据用户输入记录不合格的数据ID
            if user_input == "1":
                data_id = data['source']["id"]  # 假设id字段为"data_id"
                # 在这里你可以根据实际情况将数据ID保存到一个列表或者其他数据结构中
                invalid_ids.append(data_id)
            print()  # 打印空行分隔数据
    return invalid_ids


direction = "en2cn"
invalid_ids = process_jsonl_file("data/"+direction+"_sampled_gold_test.jsonl")
print("direction:", direction)
print("ingredient:", invalid_ids)
import pdb;pdb.set_trace()