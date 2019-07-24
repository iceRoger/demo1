from db import db_handler
from lib import common

bank_logger = common.get_logger('bank')

# 提现接口
def withdraw_interface(user, money):

    user_dic = db_handler.select(user)

    if user_dic['balance'] >= money * 1.05:

        user_dic['balance'] -= money * 1.05

        msg = f'用户[{user}] 提现[{money}]元成功!'

        user_dic['flow'].append(msg)

        db_handler.save(user_dic)

        return True, msg

    return False, '余额不足!'


# 还款接口
def repay_interface(user, money):
    user_dic = db_handler.select(user)

    user_dic['balance'] += money

    msg = f'用户{user}, 还款{money}元成功!'
    user_dic['flow'].append(msg)

    db_handler.save(user_dic)

    return True, msg


# 转账接口
def transfer_interface(to_user, from_user, money):

    to_user_dic = db_handler.select(to_user)

    from_user_dic = db_handler.select(from_user)

    if from_user_dic['balance'] >= money:

        # 加减钱操作
        from_user_dic['balance'] -= money

        to_user_dic['balance'] += money

        # 拼接流水信息
        to_user_flow = f'{to_user}用户接收到用户{from_user}转账{money}元'
        from_user_flow = f'{from_user}用户给到用户{to_user}转账{money}元'

        # 记录流水
        from_user_dic['flow'].append(from_user_flow)
        to_user_dic['flow'].append(to_user_flow)

        # 保存用户信息
        db_handler.save(from_user_dic)
        db_handler.save(to_user_dic)

        return True, from_user_flow

    return False, '余额不足,请充值!'


# 查看流水接口
def check_flow_interface(user):
    user_dic = db_handler.select(user)

    return user_dic['flow']


# 银行支付接口
def pay_interface(user, cost):
    user_dic = db_handler.select(user)

    if user_dic['balance'] >= cost:

        user_dic['balance'] -= cost

        user_dic['flow'].append(f'{user}用户支付{cost}成功!')

        db_handler.save(user_dic)

        return True

    else:
        return False
