# import numpy as np
import random
import math
import datetime
import pandas as pd
from main_copy import pack_products_into_restrictions

item_sets = [[9, 9, 9], [2, 2, 2], [1, 1, 1], [1, 1, 1], [2, 2, 2]]
Box = (13, 17, 30)

item_sets.sort(key=lambda x: (x[0] * x[1] * x[2]), reverse=True)  # 将箱子按从大到小排列
item_sets = [sorted(i, reverse=True) for i in item_sets]  # 将箱子的摆放顺序统一

def exchange_item(items):  # 第一类邻域选择，随机交换两个物品
    s1, s2 = random.randint(0, len(items) - 1), random.randint(0, len(items) - 1)
    while s1 == s2:
        s2 = random.randint(0, len(item_sets) - 1)
    items[s1], items[s2], = items[s2], items[s1]
    return items

def exchange_direction(items):  # 第二类邻域选择，随机交换某个物品的方向
    s = random.randint(0, len(items) - 1)
    item = items[s]
    s_1, s_2 = random.randint(0, len(item) - 1), random.randint(0, len(item) - 1)
    while s_1 == s_2:
        s_2 = random.randint(0, len(item) - 1)
    item[s_1], item[s_2], = item[s_2], item[s_1]
    items[s] = item
    return items


def sa(alpha, t_set, items_sa, box_sa, markovlen):
    # alpha = 0.99
    # t = (1, 100)
    # m = 100
    min_t = t_set[0]
    t = t_set[1]
    valuecurrent = pack_products_into_restrictions(items_sa,box_sa)[0]
    valuebest = valuecurrent
    itemscurrent = items_sa
    result = []  # 记录迭代过程中的最优解
    while t > min_t:
        for i in range(markovlen):
            # 倒序+插段
            if random.random() > 0.5:  # 交换路径中的这2个节点的顺序
                itemsnew = exchange_item(items_sa)
            else:  # 交换次序
                itemsnew = exchange_direction(items_sa)

            valuenew, select_items = pack_products_into_restrictions(items_sa,box_sa)
            # print (valuenew)
            if valuenew >= valuecurrent:  # 接受该解
                r = 0
                # 更新solutioncurrent 和solutionbest
                valuecurrent = valuenew
                itemscurrent = itemsnew.copy()
                if valuenew >= valuebest:
                    valuebest = valuenew
                    itemsbest = select_items.copy()
            else:  # 按一定的概率接受该解
                if random.random() <= math.exp(-(valuecurrent - valuenew) / t):
                    # if np.random.rand() < (2/math.pi) * math.atan((valuenew - valuecurrent) * 0.000001*t):
                    valuecurrent = valuenew
                    itemscurrent = itemscurrent.copy()
                else:
                    itemsnew = itemscurrent.copy()
            t = alpha * t
        # result.append(itemsbest)
            print('temp:', t)
            print('itemsbest', itemsbest)
            print('valuebest', valuebest)

s1 = datetime.datetime.now()
sa(0.99, (0.001, 1), [[8, 8, 9], [7, 5, 8], [7, 4, 2], [1, 2, 1], [2, 2, 1], [1, 1, 3], [4, 2, 2], [2, 2, 1], \
                    [1, 1, 3], [4, 2, 2], [2, 2, 1], [1, 1, 3], [4, 2, 2], [4, 4, 4], [3, 3, 3]], (10, 10, 10), 1)
s2 = datetime.datetime.now()
print('time:', s2 - s1)

#  pack_products_into_restrictions(item_sets, Box)
