import random  # 导入random模块，用于生成随机数
import heapq  # 导入heapq模块，用于实现优先队列
import matplotlib.pyplot as plt  # 导入matplotlib.pyplot模块，用于绘制图形

# 定义一个名为Robot的类
class Robot:
    # 初始化方法，设置机器人的属性
    def __init__(self, graph, node_data, robot_type, speed, capacity):
        self.graph = graph  # 图形，表示机器人可以移动的区域
        self.node_data = node_data  # 节点数据，表示每个节点的信息
        self.robot_type = robot_type  # 机器人类型，用于确定机器人可以访问哪些节点
        self.speed = speed  # 机器人的速度
        self.capacity = capacity  # 机器人的容量，表示机器人可以携带的物品数量
        self.path = []  # 机器人的路径，记录机器人访问过的节点
        self.time = 0  # 机器人的时间，记录机器人工作的总时间

    # 定义一个名为work的方法，模拟机器人的工作过程
    def work(self):
        # 当还有未访问的节点时，机器人继续工作
        while any(data[2] > 0 for data in self.node_data):
            self.visit_nodes()  # 访问节点
            self.return_to_center()  # 返回中心
        return self.path, self.time  # 返回机器人的路径和总时间

    # 定义一个名为visit_nodes的方法，模拟机器人访问节点的过程
    def visit_nodes(self):
        # 当机器人的容量大于0且还有未访问的节点时，机器人继续访问节点
        while self.capacity > 0 and any(data[2] > 0 for data in self.node_data):
            node = self.find_next_node()  # 寻找下一个节点
            if node is None:  # 如果没有下一个节点，结束访问
                break
            self.visit_node(node)  # 访问节点

    # 定义一个名为find_next_node的方法，寻找下一个节点
    def find_next_node(self):
        # 找出所有未访问的节点
        unvisited_nodes = [i for i, data in enumerate(self.node_data) if data[2] > 0]
        if not unvisited_nodes:  # 如果没有未访问的节点，返回None
            return None
        return random.choice(unvisited_nodes)  # 随机选择一个未访问的节点

    # 定义一个名为visit_node的方法，访问节点
    def visit_node(self, node):
        node_type = 'a' if node % 2 == 0 else 'b'  # 确定节点类型
        # 如果机器人类型和节点类型匹配，机器人可以访问该节点
        if (self.robot_type == 'a' and node_type == 'a') or (self.robot_type == 'b' and node_type == 'b'):
            goods = min(self.capacity, self.node_data[node][2])  # 确定机器人可以携带的物品数量
            self.capacity -= goods  # 更新机器人的容量
            # 更新节点数据
            self.node_data[node] = (self.node_data[node][0], self.node_data[node][1], self.node_data[node][2] - goods)
        self.path.append(node)  # 将节点添加到路径中
        # 更新机器人的时间
        self.time += self.graph[self.path[-2]][node] / self.speed if len(self.path) > 1 else 0

    # 定义一个名为return_to_center的方法，模拟机器人返回中心的过程
    def return_to_center(self):
        path = self.find_shortest_path(self.path[-1], 0)  # 寻找返回中心的最短路径
        self.path.extend(path[1:])  # 将路径添加到机器人的路径中
        # 更新机器人的时间
        self.time += sum(self.graph[path[i]][path[i+1]] for i in range(len(path)-1)) / self.speed
        self.capacity = 10  # 重置机器人的容量

    # 定义一个名为find_shortest_path的方法，寻找最短路径
    def find_shortest_path(self, start, end):
        distances = [float('inf')] * len(self.graph)  # 初始化所有节点到起点的距离为无穷大
        distances[start] = 0  # 起点到自身的距离为0
        pq = [(0, start)]  # 创建一个优先队列，存储节点和它们到起点的距离
        prev = [None] * len(self.graph)  # 记录每个节点的前一个节点

        # 当优先队列不为空时，继续寻找最短路径
        while pq:
            curr_dist, curr_node = heapq.heappop(pq)  # 弹出当前距离最短的节点
            if curr_node == end:  # 如果当前节点是终点，结束寻找
                break
            if curr_dist > distances[curr_node]:  # 如果当前距离大于节点到起点的距离，跳过当前节点
                continue
            # 遍历当前节点的所有邻居
            for neighbor, distance in enumerate(self.graph[curr_node]):
                if distance == 0:  # 如果邻居节点不可达，跳过当前邻居
                    continue
                new_dist = curr_dist + distance  # 计算到邻居节点的距离
                # 如果新的距离小于邻居节点到起点的距离，更新邻居节点的距离和前一个节点
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    prev[neighbor] = curr_node
                    heapq.heappush(pq, (new_dist, neighbor))  # 将邻居节点和新的距离添加到优先队列中

        path = []  # 初始化最短路径
        curr = end  # 从终点开始
        while curr is not None:  # 当前节点不为空时，继续寻找
            path.append(curr)  # 将当前节点添加到最短路径中
            curr = prev[curr]  # 更新当前节点为前一个节点
        path.reverse()  # 反转最短路径
        return path  # 返回最短路径

# 定义一个名为create_graph的函数，创建图形
def create_graph(edges):
    n = max(max(u, v) for u, v, _ in edges)  # 找出边中的最大节点
    graph = [[0] * (n+1) for _ in range(n+1)]  # 初始化图形
    for u, v, w in edges:  # 遍历所有的边
        graph[u-1][v-1] = graph[v-1][u-1] = w  # 设置边的权重
    return graph  # 返回图形

# 定义一个名为simulate的函数，模拟机器人的工作过程
def simulate(graph, node_data, num_simulations):
    times = []  # 初始化时间列表
    for _ in range(num_simulations):  # 进行指定次数的模拟
        # 创建两个机器人
        robot_a = Robot(graph, [list(data) for data in node_data], 'a', 1, 10)
        robot_b = Robot(graph, [list(data) for data in node_data], 'b', 1, 10)
        # 让两个机器人工作
        path_a, time_a = robot_a.work()
        path_b, time_b = robot_b.work()
        # 记录两个机器人的工作时间
        times.append(max(time_a, time_b))
        # 每完成10次模拟，打印一次进度
        if len(times) % 10 == 0:
            print(f"Simulation {len(times)}/{num_simulations} completed.")
    times.sort()  # 对时间进行排序
    return times  # 返回时间列表

# 定义一个名为plot_results的函数，绘制结果
def plot_results(times):
    plt.plot(range(1, len(times)+1), times)  # 绘制时间的折线图
    plt.xlabel('Simulation')  # 设置x轴的标签
    plt.ylabel('Time')  # 设置y轴的标签
    plt.title('Simulation Results')  # 设置标题
    plt.show()  # 显示图形

# 定义节点数据
data = [
    (1, 3, 0), (2, 4, 1), (3, 2, 0), (4, 5, 2), (5, 6, 0), (6, 6, 2), (7, 5, 0), (8, 2, 0), (9, 4, 0), (10, 3, 1),
    (11, 6, 0), (12, 4, 3), (13, 3, 0), (14, 6, 0), (15, 2, 0), (16, 7, 2), (17, 4, 0), (18, 2, 3), (19, 5, 0), (20, 6, 0),
    (21, 5, 2), (22, 3, 0), (23, 8, 0), (24, 3, 0), (25, 6, 2), (26, 2, 0), (27, 3, 0), (28, 4, 0), (29, 2, 2), (30, 1, 0),
    (31, 5, 0)
]

# 定义边数据
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

graph = create_graph(edges)  # 创建图形
num_simulations = 600  # 设置模拟次数
times = simulate(graph, data, num_simulations)  # 进行模拟
print(f"Best time: {times[0]}")  # 打印最好的时间
plot_results(times)  # 绘制结果