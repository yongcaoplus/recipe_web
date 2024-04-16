# -*- coding: utf-8 -*-
# @Time    : 2023/6/17 3:28 PM 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import mysql.connector
import json
import os
import csv

def read_jsonl(filename):
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for item in lines:
            data.append(json.loads(item))
    return data


def format_recipe(recipe):
    template = 'Title: {}, Ingredients: {}, Steps: {}'
    ingredients = ' '.join(recipe['ingredients'])
    steps = ' '.join(recipe['steps'])
    return template.format(recipe['title'], ingredients, steps)


def save_data2jsonl(data, save_dir, filename):
    with open(os.path.join(save_dir, filename), 'w') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def replace_reference(all_ids, human_recipes, dile_dir, save_dir, filename):
    print("start to replace reference: %s" % filename)
    print("len of human_recipes: %d" % len(human_recipes))
    new_data = []
    original_data = read_jsonl(os.path.join(dile_dir, filename))
    for recipe in human_recipes:
        recipe_index = all_ids.index(recipe['id'])
        try:
            cur_recipe = original_data[recipe_index]
        except:
            breakpoint()
        cur_recipe['references'] = [recipe['recipe']]
        new_data.append(cur_recipe)
    save_data2jsonl(new_data, save_dir, filename)
    print("successfully save data to {}".format(os.path.join(save_dir, filename)))


# 建立MySQL数据库连接
conn = mysql.connector.connect(host="localhost", user="root", password="dc75c84d3b18dbd0", database="recipe", charset='utf8mb4')

# 创建游标对象
cursor = conn.cursor()

# 执行MySQL查询语句
query = """
    SELECT r.source_id, r.direction, r.source_title, r.source_ingredients, r.source_steps, a.user_email,
    a.adapted_title, a.adapted_ingredients, a.adapted_steps, r.ref_title, r.ref_ingredients,
    r.ref_steps, a.comment
    FROM myapp_recipeadaptation r
    JOIN myapp_adaptationresults a ON r.source_id = a.source_id
    WHERE r.direction = 'cn2en'
"""

cursor.execute(query)

# 获取查询结果
results = cursor.fetchall()

source_ids = []
# 遍历结果并输出

original_data = read_jsonl('data/cn2en_sampled_gold_test.jsonl')
all_ids = [recipe['source']['id'] for recipe in original_data]
source = format_recipe(original_data[0]['source'])
reference = [format_recipe(original_data[0]['references'][0])]

golden, exist_ids = [], []
with open("data/cn2en_human_adapted_ref.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(['source_id', 'direction', 'source_title', 'source_ingredient', 'source_step', 'user_email',
                        'adapted_title', 'adapted_ingredient', 'adapted_step',
                        'retrieved_title', 'retrieved_ingredient', 'retrieved_step', 'comments'])
    for row in results:
        source_id, direction, source_title, source_ingredients, source_steps, user_email, \
        adapted_title, adapted_ingredients, adapted_steps, ref_title, ref_ingredients, \
        ref_steps, comment = row
        csvwriter.writerow(row)
    #     adapted_ingredients = adapted_ingredients.split('\r\n')
    #     adapted_steps = adapted_steps.split('\r\n')
    #     adapted_recipe = format_recipe({'title': adapted_title, 'ingredients': adapted_ingredients, 'steps': adapted_steps})
    #     if source_id not in exist_ids:
    #         exist_ids.append(source_id)
    #         golden.append({"id": source_id, "recipe": adapted_recipe})

# data_dir = "data/sampled_old_ret/"
# save_dir = "data/sampled_new_ret/"
# for filename in os.listdir(data_dir):
#     replace_reference(all_ids, golden, data_dir, save_dir, filename)
#
#
# # 关闭游标和数据库连接
# cursor.close()
# conn.close()
