# -*- coding: utf-8 -*-
# @Time    : 2023/5/21 12:13 PM 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import mysql.connector


def execute_cmd(cnx, cursor, cmd, table_name):
    cursor.execute(cmd)
    cnx.commit()
    print("{} is successfully created.".format(table_name))


def main():
    # connect database
    # 连接到MySQL数据库
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="recipe"
    )
    # 创建游标对象
    cursor = cnx.cursor()
    # 1. create user table
    table_name = "user"
    user_tb_cmd = f"""
        CREATE TABLE IF NOT EXISTS """ + table_name + """(
          `user_id` INT UNSIGNED NOT NULL,
          `user_email` VARCHAR(255)  NOT NULL
        );
    """
    execute_cmd(cnx, cursor, user_tb_cmd, table_name)

    # 2. create recipe adaptation table
    table_name = "recipe_adaptation"
    adaptation_tb_cmd = f"""
        CREATE TABLE IF NOT EXISTS """ + table_name + """(
          `user_id` INT UNSIGNED  NOT NULL,
          `direction` VARCHAR(5)  NOT NULL,
          `source_id` VARCHAR(10)  NOT NULL,
          `source_title` VARCHAR(50),
          `source_title_translated` VARCHAR(50),
          `source_ingredients` VARCHAR(255),
          `source_steps` VARCHAR(512),
          `source_dish` VARCHAR(50),
          `source_index` INT UNSIGNED,
          `ref_id` VARCHAR(10)  NOT NULL,
          `ref_title` VARCHAR(50),
          `ref_title_translated` VARCHAR(50),
          `ref_ingredients` VARCHAR(255),
          `ref_steps` VARCHAR(512),
          `ref_dish` VARCHAR(50),
          `labeled_times` INT UNSIGNED  DEFAULT 0
        );
        """
    execute_cmd(cnx, cursor, adaptation_tb_cmd, table_name)

    # 3. create recipe adaptation_results table
    table_name = "adaptation_results"
    adaptation_results_tb_cmd = f"""
        CREATE TABLE IF NOT EXISTS """ + table_name + """(
          `user_id` INT UNSIGNED  NOT NULL,
          `direction` VARCHAR(5) NOT NULL,
          `source_id` VARCHAR(10) NOT NULL,
          `adapted_title` VARCHAR(50),
          `adapted_ingredients` VARCHAR(255),
          `adapted_steps` VARCHAR(512),
          `comment` VARCHAR(512)
        );
        """
    execute_cmd(cnx, cursor, adaptation_results_tb_cmd, table_name)

    # 4. create recipe recipe_evaluation table
    table_name = "recipe_evaluation"
    recipe_evaluation_tb_cmd = f"""
        CREATE TABLE IF NOT EXISTS """ + table_name + """(
          `user_id` INT UNSIGNED NOT NULL,
          `direction` VARCHAR(255) NOT NULL,
          `source_id` VARCHAR(255) NOT NULL,
          `source_title` VARCHAR(255),
          `source_title_translated` VARCHAR(255),
          `source_ingredients` VARCHAR(255),
          `source_steps` VARCHAR(255),
          `source_dish` VARCHAR(255),
          `source_index` VARCHAR(255),
          `generated_recipe` VARCHAR(255) NOT NULL,
          `method` VARCHAR(255) NOT NULL
        );
        """
    execute_cmd(cnx, cursor, recipe_evaluation_tb_cmd, table_name)

    # 5. create recipe evaluation_results table
    table_name = "evaluation_results"
    evaluation_results_tb_cmd = f"""
        CREATE TABLE IF NOT EXISTS """ + table_name + """(
          `user_id` INT UNSIGNED NOT NULL,
          `direction` VARCHAR(5) NOT NULL,
          `source_id` VARCHAR(10) NOT NULL,
          `generated_recipe` VARCHAR(600),
          `method` VARCHAR(20) NOT NULL,
          `grammar_score` TINYINT,
          `correct_score` TINYINT,
          `preservation_score` TINYINT,
          `cultural_align_score` TINYINT,
          `comment` VARCHAR(512)
        );
        """
    execute_cmd(cnx, cursor, evaluation_results_tb_cmd, table_name)

    cursor.close()
    cnx.close()


if __name__ == '__main__':
    main()
