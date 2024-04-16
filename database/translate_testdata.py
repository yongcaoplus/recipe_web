# -*- coding: utf-8 -*-
# @Time    : 2023/5/26 2:40 PM 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import json
import pdb
from tqdm import tqdm
from googletrans import Translator


translator = Translator()


def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def translate_sentece(sentences, direction):
    if isinstance(sentences, str):
        try:
            if direction == "en2cn":
                trans_sen = translator.translate(sentences, dest="zh-CN").text
            else:
                trans_sen = translator.translate(sentences, dest="en").text
        except Exception as e:
            print(e)
            print(sentences)
            import pdb;pdb.set_trace()
        return trans_sen
    else:
        ret = []
        for sentence in sentences:
            try:
                if direction == "en2cn":
                    trans_sen = translator.translate(sentence, dest="zh-CN").text
                else:
                    trans_sen = translator.translate(sentence, dest="en").text
                ret.append(trans_sen)
            except Exception as e:
                print(e)
                print(sentence)
                import pdb;pdb.set_trace()
        return ret


def translate_recipe_by_direction(recipe, direction):
    if recipe['source']["title_translated"] is None:
        recipe['source']["title_translated"] = translate_sentece(recipe['source']["title"], direction)
    recipe['source']["ingredients_translated"] = translate_sentece(recipe['source']["ingredients"], direction)
    recipe['source']["steps_translated"] = translate_sentece(recipe['source']["steps"], direction)
    return recipe


# translate recipe by using google translation api
def translate_recipe(direction):
    file_name = "/home/cy/recipe_web/database/data/" + direction + "_sampled_gold_test.jsonl"
    save_name = "/home/cy/recipe_web/database/data/" + direction + "_sampled_gold_test_w_translation.jsonl"
    recipe_data = read_jsonl_file(file_name)
    recipe_translated = []
    for recipe in tqdm(recipe_data):
        recipe_translated.append(translate_recipe_by_direction(recipe, direction))
    with open(save_name, 'w') as f:
        for recipe in recipe_translated:
            f.write(json.dumps(recipe, ensure_ascii=False) + "\n")


translate_recipe("en2cn")
translate_recipe("cn2en")