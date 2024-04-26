import numpy as np
from scipy import interpolate
import pylab as pl

data = [[0, 0], [1, 2], [2, 3], [3, 8], [4, 2], [5, 7], [6, 8]]
x = [data[i][0] for i in range(len(data))]
y = [data[i][1] for i in range(len(data))]

xnew = np.linspace(0, 6, 101)  # 用于画出插值曲线

pl.plot(x, y, "ro")

for kind in ["linear", "quadratic", "cubic"]:  # 插值方式1,2,3次多项式插值
    # linear 线性插值
    # quadratic 二次多项式插值
    # cubic 三次多项式插值
    f = interpolate.interp1d(x, y, kind=kind)  # 选择对应方式的分段插值

    ynew = f(xnew)  # 把 x 值代入插值函数, 得到 y 坐标用于画出插值曲线
    pl.plot(xnew, ynew, label=str(kind))  # label用来显示图例

f4 = interpolate.splrep(x, y)  # 3次样条插值
ynew4 = interpolate.splev(xnew, f4, der=0)
pl.plot(xnew, ynew4, label=str("cubic spline"))  # label用来显示图例

pl.legend(loc="lower right")  # 显示图例的位置
pl.show()