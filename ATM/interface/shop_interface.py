from interface import bank_interface
from db import db_handler
from lib import common

shop_logger = common.get_logger('shop')

# 商城结账接口
def buy_shop_interface(user, cost):

    flag = bank_interface.pay_interface(user, cost)

    if flag:

        return True, '购物成功!'

    else:
        return False, '余额不足,支付失败!'


# 添加购物车接口
def add_shop_cart_interface(user, shop_cart):
    user_dic = db_handler.select(user)

    old_cart = user_dic['shop_cart']

    # 循环当前购物车
    for shop in shop_cart:

        if shop in old_cart:
            # 获取当前购物车中的商品数量
            number = shop_cart[shop]

            # 给用户信息中的商品数量做 增值运算
            old_cart[shop] += number

        else:
            # 获取当前购物车中的商品数量
            number = shop_cart[shop]

            old_cart[shop] = number

    user_dic['shop_cart'].update(old_cart)
    db_handler.save(user_dic)
    return True, '添加购物车成功!'


# 查看购物车接口'
def check_shop_cart_interface(user):
    user_dic = db_handler.select(user)

    return user_dic['shop_cart']
