import hashlib
import logging.config
from conf import settings

# MD5加密功能
def get_md5(pwd):
    val = '天王盖地虎'
    md5 = hashlib.md5()
    md5.update(pwd.encode('utf-8'))
    md5.update(val.encode('utf-8'))
    res = md5.hexdigest()
    return res


# 登陆认证功能
def login_auth(func):
    from core import src
    def inner(*args, **kwargs):
        # 判断用户存在, 则执行被装饰函数
        if src.user_info['user']:
            res = func(*args, **kwargs)

            return res

        # 否则,执行登陆功能
        else:
            print('请先登陆')
            src.login()

    return inner


# 日志功能
def get_logger(type_name):
    logging.config.dictConfig(settings.LOGGING_DIC)
    logger = logging.getLogger(type_name)
    return logger


if __name__ == '__main__':
    res = get_md5('123')
    print(res)
    logger = get_logger('tank')
