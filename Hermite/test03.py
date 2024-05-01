import math

# 节点数据
nodes = {i: (i,) for i in range(1, 37)}  # 修改这一行,包含节点35和36
nodes[32] = (32, 33)  # 机器人A和B的驻地
nodes[33] = (34,)  # 图书馆

# 边数据
edges = [
    (33, 1, 0.6), (1, 2, 0.3), (2, 3, 1.1), (3, 4, 0.5), (4, 5, 0.8), (33, 6, 0.7), (1, 7, 0.6), (2, 8, 1.5),
    (3, 9, 1.7), (4, 10, 2), (5, 11, 0.7), (6, 7, 0.5), (7, 8, 1.2), (8, 9, 1.8), (9, 10, 0.8), (10, 11, 1),
    (6, 12, 0.7), (7, 13, 1.1), (8, 35, 1.3), (9, 34, 0.7), (10, 14, 1), (11, 15, 0.6), (12, 13, 0.4), (13, 35, 1.1),
    (35, 34, 2.2), (34, 14, 0.7), (14, 15, 1), (12, 16, 0.5), (13, 17, 0.7), (35, 18, 1), (34, 36, 0.4), (14, 19, 0.5),
    (15, 20, 0.6), (16, 17, 0.9), (17, 18, 0.4), (36, 19, 0.5), (19, 20, 0.6), (16, 21, 1.1), (17, 22, 0.6), (18, 23, 0.3),
    (36, 24, 0.8), (19, 25, 0.6), (20, 26, 0.4), (21, 22, 0.3), (22, 23, 1.1), (23, 24, 2.1), (24, 25, 0.8), (25, 26, 1.1),
    (21, 27, 0.5), (22, 28, 0.9), (23, 29, 0.8), (24, 30, 0.7), (25, 31, 0.5), (26, 32, 0.3), (27, 28, 0.4), (28, 29, 0.9),
    (29, 30, 1.4), (30, 31, 0.6), (31, 32, 0.5)
]

# 借还书数据
book_data = [
    (1, 3, 0), (2, 4, 1), (3, 2, 0), (4, 5, 2), (5, 6, 0), (6, 6, 2), (7, 5, 0), (8, 2, 0), (9, 4, 0), (10, 3, 1),
    (11, 6, 0), (12, 4, 3), (13, 3, 0), (14, 6, 0), (15, 2, 0), (16, 7, 2), (17, 4, 0), (18, 2, 3), (19, 5, 0), (20, 6, 0),
    (21, 5, 2), (22, 3, 0), (23, 8, 0), (24, 3, 0), (25, 6, 2), (26, 2, 0), (27, 3, 0), (28, 4, 0), (29, 2, 2), (30, 1, 0),
    (31, 5, 0)
]

# 机器人数据
robots = {
    'A': {'speed': 8, 'capacity': 10, 'start': 32},
    'B': {'speed': 10, 'capacity': 10, 'start': 32}
}

# 构建邻接矩阵
dist = [[math.inf] * len(nodes) for _ in range(len(nodes))]
for i, j, d in edges:
    dist[i-1][j-1] = d
    dist[j-1][i-1] = d

# 预处理每个节点的还书量
return_books = [0] * len(nodes)
for i, r, _ in book_data:
    return_books[i-1] = r

def robot_dp(robot):
    speed = robots[robot]['speed']
    capacity = robots[robot]['capacity']
    start = robots[robot]['start'] - 1
    library = 33  # 图书馆节点编号

    # 初始化动态规划数组
    dp = [[[math.inf] * (capacity + 1) for _ in range(len(nodes))] for _ in range(len(nodes))]
    dp[start][start][0] = 0

    # 动态规划
    for j in range(capacity + 1):
        for i in range(len(nodes)):
            for k in range(len(nodes)):
                if dp[i][k][j] == math.inf:
                    continue
                for n in nodes[k+1]:
                    n -= 1
                    if n == k or dist[k][n] == math.inf:
                        continue
                    new_j = j + return_books[n]
                    if new_j > capacity:
                        continue
                    # 在这里添加打印语句
                    print(f"正在更新 dp[{k}][{n}][{new_j}]，值为 {dp[i][k][j] + dist[k][n] / speed}")
                    dp[k][n][new_j] = min(dp[k][n][new_j], dp[i][k][j] + dist[k][n] / speed)

    # 找到最小时间
    min_time = min(dp[i][library][j] for i in range(len(nodes)) for j in range(capacity + 1))

    # 回溯得到路径
    path = []
    i, j = library, capacity
    while i != start or j > 0:
        path.append(i+1)
        for k in range(len(nodes)):
            if dp[k][i][j] != math.inf and abs(dp[k][i][j] + dist[k][i] / speed - dp[i][i][j]) < 1e-6:
                i, j = k, j - return_books[i]
                break

    path.append(start+1)
    path.reverse()

    return min_time, path

# 计算每个机器人的最优路径
for robot in robots:
    min_time, path = robot_dp(robot)
    print(f"Robot {robot}:")
    print(f"  Minimum time: {min_time:.2f}")
    print(f"  Optimal path: {' -> '.join(map(str, path))}")
