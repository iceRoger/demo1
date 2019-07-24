from db import db_handler
from lib import common

admin_logger = common.get_logger('admin')

# 冻结用户接口
def lock_interface(user):
    user_dic = db_handler.select(user)

    user_dic['lock'] = True

    db_handler.save(user_dic)
    return f'{user}用户冻结成功!'

def unlock_interface(user):
    user_dic = db_handler.select(user)

    user_dic['lock'] = False

    db_handler.save(user_dic)
    return f'{user}用户解冻成功!'


# 修改额度接口
def change_limit_interface(user, limit):
    user_dic = db_handler.select(user)
    user_dic['balance'] = limit
    db_handler.save(user_dic)
    return f'修改用户[{user}]额度成功!'
