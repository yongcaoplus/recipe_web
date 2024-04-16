# -*- coding: utf-8 -*-
# @Time    : 2023/5/23 1:57 PM
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import json
import mysql.connector
import numpy as np
import os


# split a recipe string by title, ingredients, steps fields
def split_componition(recipe_text):
    if "Title: " in recipe_text:
        title_start = recipe_text.index("Title: ") + len("Title: ")
    elif "title: " in recipe_text:
        title_start = recipe_text.index("title: ") + len("title: ")
    else:
        title_start = recipe_text.index("Title:") + len("Title:")

    title_end = recipe_text.index(", Ingredients:")
    title = recipe_text[title_start:title_end].strip()

    if "Ingredients: " in recipe_text:
        ingredients_start = recipe_text.index("Ingredients: ") + len("Ingredients: ")
    elif "ingredients: " in recipe_text:
        ingredients_start = recipe_text.index("ingredients: ") + len("ingredients: ")
    else:
        ingredients_start = recipe_text.index("Ingredients:") + len("Ingredients:")

    ingredients_end = recipe_text.index(" Steps:")
    ingredients = recipe_text[ingredients_start:ingredients_end].strip()

    if "Steps: " in recipe_text:
        steps_start = recipe_text.index("Steps: ") + len("Steps: ")
    elif "steps: " in recipe_text:
        steps_start = recipe_text.index("steps: ") + len("steps: ")
    else:
        steps_start = recipe_text.index("Steps:") + len("Steps:")

    steps = recipe_text[steps_start:].strip()

    return {"title": title, "ingredients": ingredients, "steps": steps}


# read jsonl file as dict
def read_jsonl_file(file_path, split=False):
    data = []
    # error_file_path = []
    with open(file_path, 'r') as f:
        for line in f:
            cur_recipe = json.loads(line)
            if split:
                cur_recipe['source'] = split_componition(cur_recipe['source'])
                # cur_recipe['references'] = split_componitionnition(cur_recipe['references'][0])
            # # import pdb;pdb.set_trace()
            # try:
            #     cur_recipe['source'] = split_componition(cur_recipe['source'])
            #     cur_recipe['references'] = split_componition(cur_recipe['references'][0])
            #     # cur_recipe['prediction'] = split_componition(cur_recipe['prediction'])
            # except Exception as e:
            #     # print(e)
            #     error_file_path.append(file_path)
            #     continue
            data.append(cur_recipe)
    # print("Error:", list(set(error_file_path)))
    return data

def read_jsonl(filename):
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for item in lines:
            data.append(json.loads(item))
    return data

def write_to_mysql(direction):
    # 建立与MySQL数据库的连接
    cnx = mysql.connector.connect(host="localhost", user="root", password="dc75c84d3b18dbd0", database="recipe", charset='utf8mb4')
    cursor = cnx.cursor()
    dir_path = os.path.join("/home/caoyong/recipe_web/database/data", "results_"+direction)
    id_ref_file_path = os.path.join("/home/caoyong/recipe_web/database/data", direction+"_sampled_gold_test_w_translation.jsonl")
    id_red_data = read_jsonl_file(id_ref_file_path)
    if direction == 'cn2en':
        title2id = np.load("title2id_cn2en.npy", allow_pickle=True).item()
    else:
        title2id = np.load("title2id_en2cn.npy", allow_pickle=True).item()
    for file_name in os.listdir(dir_path):
        methods = "_".join(file_name.split("_")[2:-1])
        # print(file_name)
        if "chatglm2" not in file_name:
            continue
        # Finish TODO
        # 过滤mbart
        print(methods)
        if methods == "mbart":
            continue
        all_data = read_jsonl_file(os.path.join(dir_path, file_name), split=True)
        print("all data len: {}, method: {}. ".format(len(all_data), methods))
        save_num = 0
        for i, data in enumerate(all_data):
            # try:
            #     assert id_red_data[i]['source']['title'].strip() == data['source']['title']
            # except Exception as e:
            #     print(e)
            #     import pdb
            #     pdb.set_trace()
            # source_id = id_red_data[i]['source']['id']
            # breakpoint()
            source_title = data['source']['title']
            try:
                source_id = title2id[source_title]
            except:
                breakpoint()
            if source_id in ['57460', '146211', '543498', '179797', '146487', '56306', '304163',
                             '169521'] and direction == 'cn2en':
                continue
            if source_id in ['1291584', '32515'] and direction == 'en2cn':
                continue
            # if source_id not in en2cn_valid_id and direction == 'en2cn':
            #     continue
            # if source_id not in cn2en_valid_id and direction == 'cn2en':
            #     continue
            source_ingredients = data['source']['ingredients']
            source_steps = data['source']['steps']
            ref_recipe = data['references'][0] if len(data['references']) > 0 else ""
            generated_recipe = data['prediction']
            try:
                # 插入数据到Recipes表
                insert_query = "INSERT INTO myapp_recipeevaluation (direction, source_id, source_title, source_ingredients, source_steps, ref_recipe, generated_recipe, methods, evaluated_times) " \
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (direction, source_id, source_title, source_ingredients, source_steps, ref_recipe, generated_recipe, methods, 0)
                cursor.execute(insert_query, values)
                cnx.commit()
            except Exception as e:
                print(e)
                import pdb
                pdb.set_trace()
            # print(direction, source_id, source_title, source_ingredients, source_steps, ref_recipe, generated_recipe, methods, 0)
            # breakpoint()
            save_num += 1
        print(file_name, "  Total write: ", save_num, "rows")
    # 关闭数据库连接
    cursor.close()
    cnx.close()


def save_human_set_id():
    for direction in ['en2cn', 'cn2en']:
        if direction == 'en2cn':
            all_recipes = read_jsonl_file("data/en2cn_sampled_gold_test_w_translation.jsonl")
        else:
            all_recipes = read_jsonl_file("data/cn2en_sampled_gold_test_w_translation.jsonl")
        recipe_title2id = {item['source']['title'].strip():item['source']['id'] for item in all_recipes}
        print(len(recipe_title2id), direction)
        np.save("title2id_" + direction + ".npy", recipe_title2id)

# write_to_mysql("cn2en")
write_to_mysql("en2cn")
# # write_to_mysql("cn2en")

# save_human_set_id()