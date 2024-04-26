import math
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_li(xi, x_set=[]):
    def li(Lx):
        W = 1
        c = 1
        for each_x in x_set:
            if each_x == xi:
                continue
            W = W * (Lx - each_x)

        for each_x in x_set:
            if each_x == xi:
                continue
            c = c * (xi - each_x)

        # 这里一定要转成float类型，否则极易出现严重错误. 原因就不说了(截断误差)
        return W / float(c)

    return li


def get_basis_func_alpha(xi, x_set=[]):
    def basis_func_alpha(x):
        tmp_sum = 0
        for each_x in x_set:
            if each_x == xi:
                continue
            tmp_sum = tmp_sum + 1 / float(xi - each_x)

        return (1 + 2 * (xi - x) * tmp_sum) * ((get_li(xi, x_set))(x)) ** 2

    return basis_func_alpha


def get_basis_func_beta(xi, x_set=[]):
    return lambda x: (x - xi) * ((get_li(xi, x_set))(x)) ** 2


def get_Hermite_interpolation(x=[], fx=[], deriv=[]):
    set_of_func_alpha = []
    set_of_func_beta = []
    for each in x:
        tmp_func = get_basis_func_alpha(each, x)
        set_of_func_alpha.append(tmp_func)
        tmp_func = get_basis_func_beta(each, x)
        set_of_func_beta.append(tmp_func)

    def Hermite_interpolation(Hx):
        result = 0
        for index in range(len(x)):
            result = result + fx[index] * set_of_func_alpha[index](Hx) + deriv[index] * set_of_func_beta[index](Hx)
        return result

    return Hermite_interpolation


if __name__ == '__main__':
    data=[[0,0], [1,2]]

    x_values = [point[0] for point in data]
    y_values = [point[1] for point in data]
    derivatives = [0] * len(x_values)

    Hx = get_Hermite_interpolation(x_values, y_values, derivatives)

    tmp_x = [i * 0.1 * math.pi for i in range(-20, 20)]
    tmp_y = [Hx(i) for i in tmp_x]

    # 转换正无穷大为 NaN
    tmp_x = np.array(tmp_x)
    tmp_y = np.array(tmp_y)
    tmp_x[np.isinf(tmp_x)] = np.nan
    tmp_y[np.isinf(tmp_y)] = np.nan

    plt.figure("Hermite Interpolation")
    ax1 = plt.subplot(211)

    # 使用 Seaborn 绘制原始数据散点图
    sns.scatterplot(x=[point[0] for point in data], y=[point[1] for point in data], color='b', ax=ax1)

    # 使用 Seaborn 绘制插值结果线图
    sns.lineplot(x=tmp_x, y=tmp_y, color='r', ax=ax1)

    # 设置横纵坐标的上限为 -3 到 3
    plt.xlim(-3, 3)  # 设置 x 轴的上限
    plt.ylim(-3, 3)  # 设置 y 轴的上限

    plt.show()
