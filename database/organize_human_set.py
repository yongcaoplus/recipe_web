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

direction = "cn2en"
original_recipes = read_jsonl('data/'+direction+'_sampled_gold_test.jsonl')
human_recipes = read_jsonl('data/sampled_golden_human_'+direction+'.jsonl')
for filename in os.listdir('data/silver_'+direction):
    file_path = os.path.join('data/silver_'+direction, filename)
    model_recipes = read_jsonl(file_path)
    print(len(original_recipes), len(human_recipes), len(model_recipes))
    update_model_recipes = []
    all_recipe_ids_human = [item['source_id'] for item in human_recipes]
    for original_recipe, model_recipe in zip(original_recipes, model_recipes):
        if original_recipe['source']['id'] in all_recipe_ids_human:
            human_index = all_recipe_ids_human.index(original_recipe['source']['id'])
            model_recipe['references'] = [human_recipes[human_index]['prediction'].replace("\t\t", " ")]
            update_model_recipes.append(model_recipe)
    save_data2jsonl(update_model_recipes, 'data/human_'+direction, filename.replace("silver", "human"))
    # breakpoint()

