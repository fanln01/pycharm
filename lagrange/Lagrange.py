from matplotlib import pyplot as plt
import seaborn as sns

# 定义一个函数Lg，接受两个参数：data为训练数据，格式为列表的列表，每个子列表包含两个元素，分别表示 x 和 y 值；
# testdata为要预测的数据点的 x 值
from matplotlib import pyplot as plt

def Lg(data, testdata):
    predict = 0
    data_x = [data[i][0] for i in range(len(data))]
    data_y = [data[i][1] for i in range(len(data))]
    if testdata in data_x:
        #print "testdata is already known"
        return data_y[data_x.index(testdata)]
    for i in range(len(data_x)):
        af = 1
        for j in range(len(data_x)):
            if j != i:
                af *= (1.0 * (testdata - data_x[j]) / (data_x[i] - data_x[j]))
        predict += data_y[i] * af
    return predict
def plot(data, nums):
    # 提取数据中的 x 和 y 值
    data_x = [data[i][0] for i in range(len(data))]
    data_y = [data[i][1] for i in range(len(data))]

    # 确定区域范围
    Area = [min(data_x), max(data_x)]

    # 在区域范围内生成一系列 X 值
    X = [Area[0] + 1.0 * i * (Area[1] - Area[0]) / nums for i in range(nums)]
    X[len(X) - 1] = Area[1]

    # 计算对应的 Y 值
    Y = [Lg(data, x) for x in X]

    # 绘制结果曲线
    plt.plot(X, Y, label='result')

    # 绘制数据点
    for i in range(len(data_x)):
        plt.plot(data_x[i], data_y[i], 'ro', label="point")

    # 保存图像并显示
    plt.savefig('Lg.jpg')
    plt.show()

#线性插值

data=[[0,0], [1,2]]

print(Lg(data, 1.5))

plot(data, 100)

def plot(data, nums):
    data_x = [data[i][0] for i in range(len(data))]
    data_y = [data[i][1] for i in range(len(data))]

    Area = [min(data_x), max(data_x)]

    X = [Area[0] + 1.0 * i * (Area[1] - Area[0]) / nums for i in range(nums)]
    X[len(X) - 1] = Area[1]

    Y = [Lg(data, x) for x in X]

    sns.set()  # 应用 seaborn 样式

    plt.plot(X, Y, label='result')

    for i in range(len(data_x)):
        plt.plot(data_x[i], data_y[i], 'ro', label="point")

    plt.savefig('Lg.jpg')
    plt.show()

#二次多项式插值

data=[[0,0], [1,2], [2,3]]

print(Lg(data, 1.5))

plot(data, 100)

#四次多项式插值

data=[[0,0], [1,2], [2,3], [3,8]]

print(Lg(data, 1.5))

plot(data, 100)

#五次多项式插值

data=[[0,0], [1,2], [2,3], [3,8], [4,2]]
print(Lg(data, 1.5))

plot(data, 100)

#六次多项式插值

data=[[0,0], [1,2], [2,3], [3,8], [4,2], [5,7]]

print(Lg(data,1.5))

plot(data, 100)

#七次多项式插值

data=[[0,0], [1,2], [2,3], [3,8], [4,2], [5,7], [6,8]]

print(Lg(data, 1.5))

plot(data, 100)