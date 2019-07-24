from interface import user_interface
from lib import common
from interface import bank_interface
from interface import shop_interface
from interface import admin_interface


user_info = {
    'user': None,
}


# 注册
def register():
    print('注册功能...')
    while True:
        user = input('请输入用户名: ').strip()

        # 调用接口判断用户是否存在
        flag = user_interface.check_user_interface(user)

        # 若存在,则让用户重新输入
        if flag:

            print('用户已存在, 请重新输入!')

            continue

        pwd = input('请输入密码: ').strip()
        re_pwd = input('请确认密码: ').strip()

        if pwd == re_pwd:

            # 业务逻辑
            # 调用接口层注册接口保存用户信息
            msg = user_interface.register_interface(user, pwd)
            if msg:
                print(msg)
                break
            else:
                print('注册失败!')
        else:
            print('密码不一致.')

            # user_dic = {
            #     'user': user,
            #     'pwd': pwd,
            #     'balance': 15000
            # }

            # 数据处理
            # import os
            # import json
            # base_path = os.path.dirname(os.path.dirname(__file__))
            # db_path = os.path.join(base_path, 'db')
            #
            # with open(f'{db_path}/{user}.json', 'w', encoding='utf-8') as f:
            #     json.dump(user_dic, f)
            #     f.flush()
            #     print(f'{user}用户注册成功!')
            #     break


# 登陆
def login():
    while True:
        user = input('请输入用户名: ').strip()

        flag = user_interface.check_user_interface(user)

        if not flag:
            print('用户不存在,请重新输入')
            continue

        pwd = input('请输入密码: ').strip()

        # (True, f'{user}登陆成功!') = user_interface.login_interface(user, pwd)
        # 调用登陆接口

        flag, msg = user_interface.login_interface(user, pwd)

        if flag:
            print(msg)

            # 登陆成功后做一个记录
            user_info['user'] = user

            break

        else:
            print(msg)


# 查看余额
@common.login_auth
def check_bal():
    print('查看余额...')
    bal = user_interface.check_bal_interface(user_info['user'])
    print(bal)


# 提现
@common.login_auth
def withdraw():
    while True:
        money = input('请输入提现金额: ').strip()

        if not money.isdigit():
            print('请输入数字!')
            continue

        money = int(money)
        flag, msg = bank_interface.withdraw_interface(
            user_info['user'], money)

        if flag:
            print(msg)
            break

        else:
            print(msg)


# 还款
@common.login_auth
def repay():
    while True:

        money = input('请输入还款金额: ').strip()

        if not money.isdigit():
            print('请输入数字')
            continue

        money = int(money)

        flag, msg = bank_interface.repay_interface(user_info['user'], money)
        if flag:
            print(msg)
            break


# 转账
@common.login_auth
def transfer():
    while True:

        to_user = input('请输入转账目标用户:').strip()
        # 判断目标用户是否存在
        flag = user_interface.check_user_interface(to_user)

        if not flag:
            print('目标用户不存在!')
            continue

        # 输入转账金额
        money = input('请输入转账金额:').strip()
        if not money.isdigit():
            print('请输入数字!')
            continue

        money = int(money)

        flag, msg = bank_interface.transfer_interface(
            to_user, user_info['user'], money)

        if flag:
            print(msg)
            break

        else:
            print(msg)


# 查看流水
@common.login_auth
def check_flow():
    flow_list = bank_interface.check_flow_interface(user_info['user'])
    for flow in flow_list:
        print(flow)

# 购物车功能
@common.login_auth
def shopping():
    good_list = [
        ['J哥牌辣椒酱', 5],
        ['Egon牌公仔', 10],
        ['nick牌T-shirt', 100],
        ['围城', 39],
        ['tank牌坦克', 50000],
    ]

    user_bal = user_interface.check_bal_interface(user_info['user'])

    shop_cart = {}

    cost = 0

    while True:

        # 打印商品信息
        for index, good_price in enumerate(good_list):
            print(index, good_price)

        # 选择商品编号或者输入q退出
        choice = input('请选择商品编号或者输入q退出').strip()

        if choice.isdigit():
            choice = int(choice)

            if choice >= 0 and choice < len(good_list):

                good_name, good_price = good_list[choice]

                if user_bal >= good_price:
                    if good_name in shop_cart:
                        shop_cart[good_name] += 1
                    else:
                        shop_cart[good_name] = 1

                    cost += good_price
                else:
                    print('*穷*, 请打工赚钱再来购买!')
            else:
                print('请输入正确商品编号.')

        elif choice == 'q':

            commit = input('是否确认结账,请输入y/n: ').strip()

            if commit == 'y':

                # 调用购车商城支付功能, 并调用银行支付接口
                flag, msg = shop_interface.buy_shop_interface(
                    user_info['user'], cost)

                if flag:
                    print(msg)
                    break

                else:
                    print(msg)

            elif commit == 'n':

                # 调用添加购物车接口
                shop_interface.add_shop_cart_interface(user_info['user'], shop_cart)

                break


# 查看购物车
@common.login_auth
def check_shop_cart():
    shop_cart = shop_interface.check_shop_cart_interface(user_info['user'])
    if not shop_cart:
        print('购物车是空的,请选择购物车功能.')

    print(shop_cart)


# 注销
@common.login_auth
def logout():
    flag, msg = user_interface.logout_interface()
    if flag:
        print(msg)


# 冻结用户功能
def lock_user():
    print('冻结用户...')
    user = input('请输入需要冻结的用户: ').strip()

    flag = user_interface.check_user_interface(user)

    if flag:

        # 调用冻结接口
        msg = admin_interface.lock_interface(user)
        print(msg)

    else:
        print('用户不存在!')


# 解冻用户功能
def unlock_user():
    print('解冻用户...')

    user = input('请输入需要解冻的用户: ').strip()

    flag = user_interface.check_user_interface(user)

    if flag:

        # 调用冻结接口
        msg = admin_interface.unlock_interface(user)
        print(msg)

    else:
        print('用户不存在!')


# 修改用户额度
def change_limit():
    print('修改用户额度')
    user = input('请输入需要修改额度的用户: ').strip()

    flag = user_interface.check_user_interface(user)
    if not flag:
        print('用户不存在!')
        return

    limit = input('请输入修改额度').strip()

    if limit.isdigit():
        limit = int(limit)

        # 调用修改额度接口
        msg = admin_interface.change_limit_interface(user, limit)
        print(msg)

    else:
        print('请输入数字')


admin_func_dic = {
    '1': lock_user,
    '2': unlock_user,
    '3': change_limit,
}
# 管理员功能
@common.login_auth
def admin_sys():
    while True:
        print('''
        1.冻结用户
        2.解冻用户
        3.用户额度
        ''')

        choice = input('请选择管理员功能: ').strip()

        if choice not in admin_func_dic:
            print('请重新输入')
            continue

        admin_func_dic[choice]()


# 字典容器
func_dic = {
    '1': register,
    '2': login,
    '3': check_bal,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_cart,
    '10': logout,
    '11': admin_sys,
}

def run():
    while True:
        print('''
        1.注册
        2.登陆
        3.查看余额
        4.提现
        5.还款
        6.转账
        7.查看流水
        8.购物车功能
        9.查看购物车
        10.注销
        11.管理员功能
        ''')

        choice = input('请选择功能编号: ').strip()

        if choice == 'q':
            break

        if choice in func_dic:

            func_dic[choice]()

        else:
            print('请输入正确编号')

