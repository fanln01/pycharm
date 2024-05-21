import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.optimize import leastsq

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

x = np.arange(0, 10, 1, dtype='float')
y = np.array([67.052, 68.008, 69.803, 72.024, 73.400, 72.063, 74.669, 74.487, 74.065, 76.777], dtype='float')

# param:最小化时的初值fun:拟合函数
# 二次
param0 = [0, 0, 0]
def quadratic_fun(s, x):  # s代表待定系数列表
    k1, k2, b = s
    return k1 * x + k2 * x ** 2 + b

# 三次
param1 = [0, 0, 0, 0]
def cubic_fun(s, x):
    k1, k2, k3, b = s
    return k1 * x ** 3 + k2 * x**2 + k3 * x + b

# 四次
param2 = [0, 0, 0, 0, 0]
def fpower_fun(s, x):
    k1, k2, k3, k4, b = s
    return k1 * x ** 4 + k2 * x**3 + k3 * x**2 + k4 * x + b

# 自定义函数
param3 = [0, 0, 0]
def myfuns(s, x):
    a, b, c = s
    return a * np.exp(-b * (x - c))

# 求出残差
def dist(a, fun, x, y):
    return fun(a, x) - y

funs = [quadratic_fun, cubic_fun, fpower_fun, myfuns]
params = [param0, param1, param2, param3]
colors = ['blue', 'red', 'black', 'green']
fun_name = ['一次', '二次', '三次', 'a*exp(-b*(t-c))']

# 作图
plt.figure()
plt.title(u'石油产量年际变化')
plt.xlabel(u't/h')
plt.ylabel(u'T/摄氏度')
# 坐标轴的范围xmin, xmax, ymin, ymax
plt.axis([0, 11, 60, 80])
plt.grid(True)
plt.plot(x, y, 'k.', label='sample data')

for i, (func, param, color, name) in enumerate(zip(funs, params, colors, fun_name)):
    var = leastsq(dist, param, args=(func, x, y))  # 求出残差平方和最小的待定系数值
    plt.plot(x, func(var[0], x), color, label=name)
    print('[%s] —预测: %.4f, abs(bias): %.4f, bias-std: %.4f' % (name,
                                                                 ((y - func(var[0], x)) ** 2).sum(),  # 二范数平方
                                                                 (y - func(var[0], x)).std(),  # 残差的标准差
                                                                 (abs(y - func(var[0], x))).mean()))  # 残差绝对值的均值
    # 预测 x=18 处的值
    x_pred = 10
    y_pred = func(var[0], x_pred)
    print(f"预测 x={x_pred} 处的值为: {y_pred}")

plt.legend(loc='upper left')
plt.show()

for i, (func, param, color, name) in enumerate(zip(funs, params, colors, fun_name)):
    var = leastsq(dist, param, args=(func, x, y))
    print(f"函数: {name}")
    print(f"拟合参数: {var[0]}")
    print(f"残差平方和: {sum(dist(var[0], func, x, y) ** 2)}")
    # 预测 x=18 处的值
    x_pred
