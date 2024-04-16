import json
import mysql.connector
from tqdm import tqdm

# read jsonl file as dict
def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data


def write_to_mysql(direction):
    # 建立与MySQL数据库的连接
    cnx = mysql.connector.connect(host="localhost", user="root", password="dc75c84d3b18dbd0", database="recipe", charset='utf8mb4')
    cursor = cnx.cursor()
    file_name = "data/" + direction + "_sampled_gold_test_w_translation.jsonl"
    print("writing:", file_name)
    print("Direction:", direction)
    for i, data in tqdm(enumerate(read_jsonl_file(file_name))):
        # if i >= 5:
        #     break
        # 提取所需字段
        source_title = data['source']['title']
        source_title_translated = data['source']['title_translated']
        source_ingredients = '\t\t'.join(data['source']['ingredients'])
        source_ingredients_translated = '\t\t'.join(data['source']['ingredients_translated'])
        source_steps = '\t\t'.join(data['source']['steps'])
        source_steps_translated = '\t\t'.join(data['source']['steps_translated'])
        source_dish = data['source']['dish']
        source_id = data['source']['id']
        source_index = data['source_index']
        ref_id = data['references'][0]['id']
        ref_title = data['references'][0]['title']
        ref_title_translated = data['references'][0]['title_translated']
        ref_ingredients = '\t\t'.join(data['references'][0]['ingredients'])
        ref_steps = '\t\t'.join(data['references'][0]['steps'])
        ref_dish = data['references'][0]['dish']
        if source_id in ['57460', '146211', '543498', '179797', '146487', '56306', '304163', '169521'] and direction == 'cn2en':
            continue
        if source_id in ['1291584', '32515'] and direction == 'en2cn':
            continue
        try:
            # 插入数据到Recipes表
            insert_query = "INSERT INTO myapp_recipeadaptation (direction, source_id, source_title, source_title_translated, source_ingredients, source_ingredients_translated, source_steps, source_steps_translated, source_dish, source_index, ref_id, ref_title, ref_title_translated, ref_ingredients, ref_steps, ref_dish, labeled_times) " \
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (
            direction, source_id, source_title, source_title_translated, source_ingredients, source_ingredients_translated, source_steps, source_steps_translated, source_dish,
            source_index, ref_id, ref_title, ref_title_translated, ref_ingredients, ref_steps, ref_dish, 0)
            cursor.execute(insert_query, values)
            cnx.commit()
        except Exception as e:
            print(e)
            import pdb;
            pdb.set_trace()
    # 关闭数据库连接
    cursor.close()
    cnx.close()
    print("Total write: ", i + 1, "rows")

write_to_mysql("en2cn")
write_to_mysql("cn2en")
