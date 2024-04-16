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

# for direction in ["en2cn", "cn2en"]:
#     original_recipes = read_jsonl('data/'+direction+'_sampled_gold_test.jsonl')  # source  src
#     human_recipes = read_jsonl('data/sampled_golden_human_'+direction+'.jsonl') # human  ref
#     for filename in os.listdir('data/silver_'+direction):  # retrieved prediction
#         file_path = os.path.join('data/silver_'+direction, filename)
#         model_recipes = read_jsonl(file_path)
#         print(len(original_recipes), len(human_recipes), len(model_recipes))
#         update_model_recipes = []
#         all_recipe_ids_human = [item['source_id'] for item in human_recipes]
#         for original_recipe, model_recipe in zip(original_recipes, model_recipes):
#             if original_recipe['source']['id'] in all_recipe_ids_human:
#                 human_index = all_recipe_ids_human.index(original_recipe['source']['id'])
#                 model_recipe['references'] = [human_recipes[human_index]['prediction'].replace("\t\t", " ")]
#                 model_recipe['prediction'] = format_recipe(original_recipe['references'][0])
#                 update_model_recipes.append(model_recipe)
#         # breakpoint()
#         save_data2jsonl(update_model_recipes, 'data/human_'+direction, filename.replace("silver", "retrival"))
#         break


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


def obtain_human_set(silver_set, human_set):
    new_human_set = []
    title2id = {item['source']['title'].strip(): item['source']['id'] for item in silver_set}
    for recipe in human_set:
        cur_recipe_components = split_componition(recipe['source'])
        cur_recipe_title = cur_recipe_components['title'].strip()
        # breakpoint()
        source_id = title2id[cur_recipe_title]
        cur_source_recipe = None
        for source_recipe in silver_set:
            if source_id == source_recipe['source']['id']:
                cur_source_recipe = source_recipe['source']
                break
        new_human_set.append({"source": cur_source_recipe, "references": recipe['references'], "source_index": -1})
    return new_human_set


silver_set = read_jsonl('data/en2cn_sampled_gold_test.jsonl')
human_set = read_jsonl('data/human_en2cn/sampled_human_mt5_base_en2cn.jsonl')
new_human_set = obtain_human_set(silver_set, human_set)
save_data2jsonl(new_human_set, 'data/', 'en2cn_human_set.jsonl')

silver_set = read_jsonl('data/cn2en_sampled_gold_test.jsonl')
human_set = read_jsonl('data/human_cn2en/sampled_human_mt5_base_cn2en.jsonl')
new_human_set = obtain_human_set(silver_set, human_set)
save_data2jsonl(new_human_set, 'data/', 'cn2en_human_set.jsonl')