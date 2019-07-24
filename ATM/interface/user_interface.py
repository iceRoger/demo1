from db import db_handler
from lib import common
from lib import common

user_logger = common.get_logger('user')

# 查看用户接口
def check_user_interface(user):

    # 调用数据处理层的select函数,查看用户信息
    user_dic = db_handler.select(user)

    if user_dic:
        return True


# 注册接口
def register_interface(user, pwd, balance=15000):

    pwd = common.get_md5(pwd)

    user_dic = {
        'user': user,
        'pwd': pwd,
        'balance': balance,
        'flow': [],
        'shop_cart': {},
        'lock': False
    }

    # 调用保存数据功能
    db_handler.save(user_dic)

    user_logger.info(f'{user_dic["user"]}用户注册成功!')

    return f'{user_dic["user"]}用户注册成功!'


# 登陆接口
def login_interface(user, pwd):

    user_dic = db_handler.select(user)

    pwd = common.get_md5(pwd)

    if user_dic['lock']:
        user_logger.info(f'用户[{user}]已被冻结,请联系管理员!')

        return False, '用户已被冻结,请联系管理员!'

    if user_dic['pwd'] == pwd:
        user_logger.info(f'{user}登陆成功!')
        return True, f'{user}登陆成功!'

    user_logger.info(f'{user}输入密码错误!')
    return False, f'{user}密码错误!'


# 查看余额接口
def check_bal_interface(user):
    user_dic = db_handler.select(user)
    return user_dic['balance']


# 注销接口
def logout_interface():
    from core import src
    user = src.user_info['user']
    src.user_info['user'] = None

    return True, f'{user}用户注销成功!欢迎官人下次再来!'



