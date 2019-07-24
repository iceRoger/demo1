import os
import json
from conf import settings


# 保存数据
def save(user_dic):

    # 拼接用户保存文件
    user_path = f'{settings.DB_PATH}/{user_dic["user"]}.json'

    # 把用户信息写入文件中
    with open(user_path, 'w', encoding='utf-8') as f:
        json.dump(user_dic, f, ensure_ascii=False)
        f.flush()


# 查看用户数据
def select(user):
    # base_path = os.path.dirname(os.path.dirname(__file__))
    # db_path = os.path.join(base_path, 'db')

    user_path = f'{settings.DB_PATH}/{user}.json'

    # 判断用户文件是否存在
    if os.path.exists(user_path):

        # 若存在, 读取用户信息
        with open(user_path, 'r', encoding='utf-8') as f:

            user_dic = json.load(f)

            return user_dic
