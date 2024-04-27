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
import seaborn as sns
import matplotlib.pyplot as plt

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


data = [[-5.0, -0.1923], [-4.5, -0.2118], [-4.0, -0.2353], [-3.5, -0.2642], [-3.0, -0.3], [-2.5, -0.3448], [-2.0, -0.4000], [-1.5, -0.4615], [-1.0, -0.5000], [-0.5, -0.4000], [0.0, 0.0], [0.5, 0.4000], [1.0, 0.5000], [1.5, 0.4615], [2.0, 0.4000], [2.5, 0.3448], [3.0, 0.3000], [3.5, 0.2642], [4.0, 0.2353], [4.5, 0.2118], [5.0, 0.1923]]
print(Lg(data, 1.5))

plot(data, 100)