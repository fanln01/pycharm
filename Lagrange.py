from matplotlib import pyplot as plt

# 定义一个函数Lg，接受两个参数：data为训练数据，格式为列表的列表，每个子列表包含两个元素，分别表示 x 和 y 值；
# testdata为要预测的数据点的 x 值
def Lg(data, testdata):

    # 初始化预测值
    predict = 0

    # 从训练数据中提取 x 值和 y 值，分别存储在 data_x 和 data_y 中
    data_x = [data[i][0] for i in range(len(data))]
    data_y = [data[i][1] for i in range(len(data))]

    # 检查测试数据是否已存在于训练数据中
    if testdata in data_x:
        # 如果测试数据的 x 值在训练数据中，则直接返回对应的 y 值
        return data_y[data_x.index(testdata)]

        # 计算预测值
    for i in range(len(data_x)):
        # 初始化亲和力函数值
        af = 1
        for j in range(len(data_x)):
            if j != i:
                # 计算亲和力函数的值，这里使用的是拉格朗日插值的核函数形式
                af *= (1.0 * (testdata - data_x[j]) / (data_x[i] - data_x[j]))
    # 计算预测值
    for i in range(len(data_x)):
        # 根据拉格朗日插值公式，计算预测值
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
