def robot_dp(robot):
    speed = robots[robot]['speed']
    capacity = robots[robot]['capacity']
    start = robots[robot]['start'] - 1
    library = 33  # 图书馆节点编号

    # 初始化动态规划数组
    dp = [[math.inf] * (capacity + 1) for _ in range(len(nodes))]
    dp[start][0] = 0

    # 记录路径
    path = [[None] * (capacity + 1) for _ in range(len(nodes))]

    # 动态规划
    for j in range(capacity + 1):
        for i in range(len(nodes)):
            if dp[i][j] == math.inf:
                continue
            for n in nodes[i+1]:
                n -= 1
                if n == i or dist[i][n] == math.inf:
                    continue
                new_j = j + return_books[n]
                if new_j > capacity:
                    continue
                new_time = dp[i][j] + dist[i][n] / speed
                if new_time < dp[n][new_j]:
                    dp[n][new_j] = new_time
                    path[n][new_j] = i

    # 找到最小时间
    min_time = min(dp[library][j] for j in range(capacity + 1))

    # 回溯得到路径
    route = []
    i, j = library, capacity
    while i != start or j > 0:
        route.append(i+1)
        i, j = path[i][j], j - return_books[i]

    route.append(start+1)
    route.reverse()

    return min_time, route