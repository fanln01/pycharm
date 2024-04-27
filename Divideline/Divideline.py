import matplotlib.pyplot as plt
import numpy as np


def DivideLine(data, testdata):
    # 找到最邻近的数据点
    data_x, data_y = data[:, 0], data[:, 1]

    if testdata in data_x:
        index = np.where(data_x == testdata)[0][0]
        return data_y[index]
    else:
        index = np.searchsorted(data_x, testdata) - 1
        if index < 0:
            index = 0
        elif index >= len(data_x) - 1:
            index = len(data_x) - 2

        x1, y1 = data_x[index], data_y[index]
        x2, y2 = data_x[index + 1], data_y[index + 1]
        predict = (testdata - x1) * (y2 - y1) / (x2 - x1) + y1
        return predict


def plot(data, nums):
    data = np.array(data)
    data_x, data_y = data[:, 0], data[:, 1]

    min_x, max_x = np.min(data_x), np.max(data_x)
    X = np.linspace(min_x, max_x, nums)

    Y = np.array([DivideLine(data, x) for x in X])

    plt.figure(figsize=(8, 6))
    plt.plot(X, Y, label='Linear Interpolation')
    plt.plot(data_x, data_y, 'ro', label='Original Data')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Piecewise Linear Interpolation')
    plt.savefig('DivLine.jpg', dpi=150)
    plt.show()


data = np.array([[-5.0, -0.1923], [-4.5, -0.2118], [-4.0, -0.2353], [-3.5, -0.2642], [-3.0, -0.3], [-2.5, -0.3448], [-2.0, -0.4000], [-1.5, -0.4615], [-1.0, -0.5000], [-0.5, -0.4000], [0.0, 0.0], [0.5, 0.4000], [1.0, 0.5000], [1.5, 0.4615], [2.0, 0.4000], [2.5, 0.3448], [3.0, 0.3000], [3.5, 0.2642], [4.0, 0.2353], [4.5, 0.2118], [5.0, 0.1923]])
print(DivideLine(data, 1.5))
plot(data, 100)