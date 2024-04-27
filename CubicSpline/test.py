# -*- coding:utf-8 -*-
"""
@brief     : 利用拉格朗日插值、分段线性插值和三次样条插值构造插值函数
"""
import numpy as np
from matplotlib import pyplot as plt
from sympy import *
from matplotlib.font_manager import FontProperties


def function(x):
    return 1 / (1 + pow(x, 2)*25)
    # return abs(x)


class Lagrange:
    def __init__(self, interval, n):
        self.interval = interval  # 插值区间
        self.num = n  # 次数
        self.h = (interval[1] - interval[0]) / n  # 插值间隔

    def cal_wn(self):
        xi = np.arange(self.interval[0], self.interval[1] + self.h / 2, self.h)
        x = symbols('x')
        wn = 1
        for i in xi:
            wn *= (x - i)
        return wn

    def cal_diff_wn(self):
        x = symbols('x')
        return diff(self.cal_wn(), x)

    def lagrange_expression(self):
        Lx = 0
        x = symbols('x')
        xi = np.arange(self.interval[0], self.interval[1] + self.h / 2, self.h)
        diff_wn = self.cal_diff_wn()
        wn = self.cal_wn()
        for i in range(self.num + 1):
            num = wn / (x - xi[i])
            li = num / diff_wn.subs('x', xi[i])
            Lx += li * function(xi[i])
        return Lx

    def show_result(self):
        x = np.linspace(self.interval[0], self.interval[1], 100)
        expression = self.lagrange_expression()
        print(expression)
        y = np.zeros((100,))
        for i in range(len(x)):
            y[i] = expression.subs('x', x[i])
        ax = plt.subplot(222)
        ax.set_title("拉格朗日插值n=10", fontproperties=font_set)
        plt.plot(x, y)


class PieceLinear:
    def __init__(self, interval, n):
        self.interval = interval  # 插值区间
        self.num = n  # 区间个数
        self.h = (interval[1] - interval[0]) / n  # 插值间隔

    def create_point(self):  # 给出插值点
        x = np.arange(self.interval[0], self.interval[1] + self.h / 2, self.h)
        y = function(x)
        return np.stack((x, y), axis=1)

    def subfun(self):  # 每个区间的子函数
        x = symbols('x')
        subfuns = []
        points = self.create_point()
        for i in range(self.num):
            subfun_i = simplify(((x - points[i + 1, 0]) * points[i, 1] / (points[i, 0] - points[i + 1, 0]) + (
                        x - points[i, 0]) * points[i + 1, 1] / (points[i + 1, 0] - points[i, 0])))
            subfuns.append(subfun_i)
        return subfuns

    def show_result(self):
        points = self.create_point()
        draw_y = np.zeros((20,))
        subfuns = self.subfun()
        for i in range(self.num):
            draw_x = np.linspace(points[i, 0], points[i + 1, 0], 20)
            for j in range(len(draw_x)):
                draw_y[j] = subfuns[i].subs('x', draw_x[j])
            ax1 = plt.subplot(223)
            ax1.set_title("分段线性插值n=10", fontproperties=font_set)
            plt.plot(draw_x, draw_y)
        ax2 = plt.subplot(221)
        ax2.set_title("原函数y=f(x)", fontproperties=font_set)
        standard_x = np.linspace(-5, 5, 500)
        standard_y = function(standard_x)
        plt.plot(standard_x, standard_y, '--')


class CubicSpline:
    def __init__(self, interval, n):
        self.interval = interval  # 插值区间
        self.num = n  # 区间数
        self.h = (interval[1] - interval[0]) / n  # 插值间隔

    def create_point(self):  # 给出插值点
        x = np.arange(self.interval[0], self.interval[1] + self.h / 2, self.h)
        y = function(x)
        return np.stack((x, y), axis=1)

    def cal_mu_and_lamda(self):  # 计算出lamda和mu
        return 1 / 2  # 所有的h均相通

    def cal_diff2(self, xi):  # 计算出二阶导
        x = Symbol('x')
        expr = function(x)
        dexpr = diff(expr, x)
        return diff(dexpr, x).subs('x', xi)

    def end_M(self):
        return 0, 0  # 自然边界条件

    def cal_d(self):  # 计算结果向量
        points = self.create_point()
        d = np.zeros((self.num - 1, 1))
        for i in range(1, self.num):
            d[i - 1] = 6 / (2 * self.h * self.h) * (points[i + 1, 1] + points[i - 1, 1] - 2 * points[i, 1])
        M0, Mn = self.end_M()
        d[0] = d[0] - self.cal_mu_and_lamda() * M0
        d[-1] = d[-1] - self.cal_mu_and_lamda() * Mn
        return d

    def cal_M_coff(self):  # 计算系数矩阵
        M_coff = np.zeros((self.num - 1, self.num - 1))
        mu = lamda = self.cal_mu_and_lamda()
        for i in range(1, self.num - 2):
            M_coff[i, i - 1] = self.cal_mu_and_lamda()
            M_coff[i, i + 1] = self.cal_mu_and_lamda()
            M_coff[i, i] = 2
        M_coff[0, 0] = M_coff[-1, -1] = 2
        M_coff[0, 1] = M_coff[-1, -2] = mu
        return M_coff

    def cal_M(self):  #
        M_coff = self.cal_M_coff()
        d = self.cal_d()
        M = np.linalg.solve(M_coff, d)
        M0 = self.end_M()[0]
        Mn = self.end_M()[1]
        M = np.vstack((M0, M))
        M = np.vstack((M, Mn))
        return M

    def cal_diff2_sx(self):
        sx0 = self.end_M()[0]
        sxn = self.end_M()[1]
        x = Symbol('x')
        diff2_sx = [None] * self.num
        M = self.cal_M()
        points = self.create_point()
        for i in range(0, self.num):
            diff2_sx[i] = M[i, 0] * (points[i, 0] - x) / (self.h) + M[i + 1, 0] * (x - points[i - 1, 0]) / (self.h)
        return diff2_sx

    def cal_sx(self):
        x = Symbol('x')
        sx = []
        M = self.cal_M()
        points = self.create_point()
        for i in range(1, len(points)):
            Ai = 1 / self.h * (points[i - 1, 1] - 1 / 6 * M[i - 1] * pow(self.h, 2))
            Bi = 1 / self.h * (points[i, 1] - 1 / 6 * M[i] * pow(self.h, 2))
            sxi = (M[i - 1] * pow(points[i, 0] - x, 3) + M[i] * pow(x - points[i - 1, 0], 3)) / (6 * self.h) + Ai * (
                        points[i, 0] - x) + Bi * (x - points[i - 1, 0])
            sx.append(sxi)
        return sx

    def show_result(self):
        sx = self.cal_sx()
        points = self.create_point()
        draw_y = np.zeros((500,))
        for i in range(len(sx)):
            draw_x = np.linspace(points[i, 0], points[i + 1, 0], 500)
            for j in range(len(draw_x)):
                draw_y[j] = sx[i][0].subs('x', draw_x[j])
            ax = plt.subplot(224)
            ax.set_title("三次样条插值n=10", fontproperties=font_set)
            plt.plot(draw_x, draw_y)
        plt.show()


if __name__ == "__main__":
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    fig = plt.figure(figsize=(8, 8))
    test1 = Lagrange([-5, 5], 10)  # 修改为插值区间为 [-5, 5]，插值次数为 10
    test1.show_result()
    test2 = PieceLinear([-5, 5], 10)  # 修改为插值区间为 [-5, 5]，插值次数为 10
    test2.show_result()
    test3 = CubicSpline([-5, 5], 10)  # 修改为插值区间为 [-5, 5]，插值次数为 10
    test3.show_result()
