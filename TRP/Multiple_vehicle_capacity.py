from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import matplotlib.pyplot as plt
import networkx as nx

distance_matrix =[
[0, 300, 1400, 1900, 2700, 1100, 600, 1800, 3100, 3900, 3400, 1800, 1700, 4500, 4000, 2300, 2400, 2800, 4700, 4600, 3400, 3700, 3000, 5000, 5300, 5000, 3900, 4300, 3800, 5200, 5800, 5300, 600, 3800, 2800, 4200],
[300, 0, 1100, 1600, 2400, 1400, 900, 1500, 2800, 3600, 3100, 2100, 2000, 4200, 3700, 2600, 2700, 3100, 4400, 4300, 3700, 4000, 3300, 4700, 5000, 4700, 4200, 4600, 4100, 5400, 5500, 5000, 900, 3500, 2800, 3900],
[1400, 1100, 0, 500, 1300, 2500, 2000, 2600, 1700, 2500, 2000, 3200, 3100, 3100, 2600, 3700, 3800, 4200, 3300, 3200, 4800, 5100, 4400, 3600, 3900, 3600, 5300, 5700, 5200, 4300, 4400, 3900, 2000, 2400, 3900, 2800],
[1900, 1600, 500, 0, 800, 3000, 2500, 3100, 2200, 2000, 1500, 3700, 3600, 3000, 2100, 4200, 4300, 4700, 3300, 2700, 5300, 5600, 4900, 4100, 3900, 3100, 5800, 6200, 5700, 4500, 3900, 3400, 2500, 2900, 4400, 3300],
[2700, 2400, 1300, 800, 0, 3800, 3300, 3900, 2500, 1700, 700, 4500, 4400, 2300, 1300, 5000, 5100, 5500, 2500, 1900, 6100, 6400, 5700, 3800, 3100, 2300, 6400, 6000, 5100, 3700, 3100, 2600, 3300, 3000, 5200, 3000],
[1100, 1400, 2500, 3000, 3800, 0, 500, 1700, 3500, 4300, 4500, 700, 1100, 4900, 5100, 1200, 1800, 2200, 5100, 5700, 2300, 2600, 2400, 4500, 5300, 6000, 2800, 3200, 3200, 4600, 5200, 5700, 700, 4200, 2200, 4600],
[600, 900, 2000, 2500, 3300, 500, 0, 1200, 3000, 3800, 4000, 1200, 1100, 4400, 4600, 1700, 1800, 2200, 4600, 5200, 2800, 3100, 2400, 4500, 5200, 5600, 3300, 3700, 3200, 4600, 5200, 5700, 1200, 3700, 2200, 4100],
[1800, 1500, 2600, 3100, 3900, 1700, 1200, 0, 1800, 2600, 3600, 2400, 2300, 3200, 4200, 2900, 2700, 2300, 3400, 4000, 4000, 3700, 2600, 3700, 4000, 4400, 4500, 4300, 3400, 4400, 4500, 4700, 2400, 2500, 1300, 2900],
[3100, 2800, 1700, 2200, 2500, 3500, 3000, 1800, 0, 800, 1800, 4200, 4000, 1400, 2400, 4700, 4300, 3900, 1600, 2200, 5400, 5100, 4000, 1900, 2200, 2600, 5300, 4900, 4000, 2600, 2700, 2900, 3700, 700, 2900, 1100],
[3900, 3600, 2500, 2000, 1700, 4300, 3800, 2600, 800, 0, 1000, 5000, 4800, 1000, 1600, 5500, 5100, 4700, 1500, 2100, 6200, 5900, 4800, 2700, 2100, 2500, 5900, 5500, 4600, 3200, 2600, 2800, 4500, 1500, 3700, 1900],
[3400, 3100, 2000, 1500, 700, 4500, 4000, 3600, 1800, 1000, 0, 5200, 5100, 1600, 600, 5700, 5800, 5500, 1800, 1200, 6200, 6200, 5200, 3100, 2400, 1600, 5700, 5300, 4400, 3000, 2400, 1900, 4000, 2300, 4500, 2300],
[1800, 2100, 3200, 3700, 4500, 700, 1200, 2400, 4200, 5000, 5200, 0, 400, 4400, 5400, 500, 1100, 1500, 4600, 5200, 1600, 1900, 1700, 3800, 4600, 5300, 2100, 2500, 2500, 3900, 4500, 5000, 1400, 3700, 1500, 4100],
[1700, 2000, 3100, 3600, 4400, 1100, 1100, 2300, 4000, 4800, 5100, 400, 0, 4000, 5000, 900, 700, 1100, 4200, 4800, 2000, 2300, 1300, 3400, 4200, 4900, 2500, 2900, 2100, 3500, 4100, 4600, 1800, 3300, 1100, 3700],
[4500, 4200, 3100, 3000, 2300, 4900, 4400, 3200, 1400, 1000, 1600, 4400, 4000, 0, 1000, 4900, 4300, 3900, 500, 1100, 5300, 5000, 3900, 1800, 1100, 1500, 4900, 4500, 3600, 2200, 1600, 1800, 5100, 700, 2900, 1000],
[4000, 3700, 2600, 2100, 1300, 5100, 4600, 4200, 2400, 1600, 600, 5400, 5000, 1000, 0, 5900, 5300, 4900, 1200, 600, 5600, 5600, 4600, 2500, 1800, 1000, 5100, 4700, 3800, 2400, 1800, 1300, 4600, 1700, 3900, 1700],
[2300, 2600, 3700, 4200, 5000, 1200, 1700, 2900, 4700, 5500, 5700, 500, 900, 4900, 5900, 0, 900, 1300, 4900, 5500, 1100, 1400, 1500, 3600, 4400, 5100, 1600, 2000, 2300, 3700, 4300, 4800, 1900, 4200, 2000, 4400],
[2400, 2700, 3800, 4300, 5100, 1800, 1800, 2700, 4300, 5100, 5800, 1100, 700, 4300, 5200, 900, 0, 400, 4000, 4600, 2000, 1700, 600, 2700, 3500, 4200, 2500, 2300, 1400, 2800, 3400, 3900, 2500, 3600, 1400, 3500],
[2800, 3100, 4200, 4700, 5500, 2200, 2200, 2300, 3900, 4700, 5500, 1500, 1100, 3900, 4900, 1300, 400, 0, 3700, 4300, 1700, 1400, 300, 2400, 3200, 3900, 2200, 2000, 1100, 2500, 3100, 3600, 2900, 3200, 1000, 3200],
[4700, 4400, 3300, 3300, 2500, 5100, 4600, 3400, 1600, 1500, 1800, 4600, 4200, 500, 1200, 5000, 4100, 3700, 0, 600, 4800, 4500, 3400, 1300, 600, 1000, 4400, 4000, 3100, 1700, 1100, 1300, 5300, 900, 3100, 500],
[4600, 4300, 3200, 2700, 1900, 5700, 5200, 4000, 2200, 2100, 1200, 5200, 4800, 1100, 600, 5600, 4700, 4300, 600, 0, 5000, 5000, 4000, 1900, 1200, 400, 4500, 4100, 3200, 1800, 1200, 700, 5200, 1500, 3700, 1100],
[3300, 3600, 4700, 5200, 6000, 2300, 2700, 3600, 5200, 6000, 6200, 1600, 1600, 5200, 5600, 1100, 900, 1300, 4800, 5000, 0, 300, 1400, 3500, 4300, 4600, 500, 900, 1800, 3200, 3800, 4300, 3000, 4500, 2300, 4300],
[3000, 3300, 4400, 4900, 5700, 2400, 2400, 3300, 4900, 5700, 6200, 1700, 1300, 4900, 5600, 1400, 600, 1000, 4500, 5000, 300, 0, 1100, 3200, 4000, 4600, 800, 900, 1800, 3200, 3800, 4300, 3100, 4200, 2000, 4000],
[3100, 3400, 4500, 5000, 5800, 2500, 2500, 2600, 4000, 4800, 5200, 1800, 1400, 3900, 4600, 1600, 700, 300, 3400, 4000, 1400, 1100, 0, 2100, 2900, 3600, 1900, 1700, 800, 2200, 2800, 3300, 3200, 3300, 1300, 2900],
[5000, 4700, 3600, 4100, 3800, 4600, 4600, 3700, 1900, 2700, 3100, 3900, 3500, 1800, 2500, 3700, 2800, 2400, 1300, 1900, 3500, 3200, 2100, 0, 800, 1900, 3400, 3000, 2100, 700, 1300, 1800, 5300, 1200, 3400, 800],
[5300, 5000, 3900, 3900, 3100, 5400, 5200, 4000, 2200, 2100, 2400, 4700, 4300, 1100, 1800, 4500, 3600, 3200, 600, 1200, 4300, 4000, 2900, 800, 0, 1100, 3800, 3400, 2500, 1100, 500, 1000, 5900, 1500, 3700, 1100],
[5000, 4700, 3600, 3100, 2300, 6100, 5600, 4400, 2600, 2500, 1600, 5400, 5000, 1500, 1000, 5200, 4300, 3900, 1000, 400, 4600, 4600, 3600, 1900, 1100, 0, 4100, 3700, 2800, 1400, 800, 300, 5600, 1900, 4100, 1500],
[3800, 4100, 5200, 5700, 6400, 2800, 3200, 4100, 5300, 5900, 5700, 2100, 2100, 4900, 5100, 1600, 1400, 1800, 4400, 4500, 500, 800, 1900, 3400, 3800, 4100, 0, 400, 1300, 2700, 3300, 3800, 3500, 4600, 2800, 4200],
[3900, 4200, 5300, 5800, 6000, 3200, 3300, 4200, 4900, 5500, 5300, 2500, 2200, 4500, 4700, 2000, 1500, 1900, 4000, 4100, 900, 900, 1700, 3000, 3400, 3700, 400, 0, 900, 2300, 2900, 3400, 3900, 4200, 2900, 3800],
[3900, 4200, 5300, 5800, 5100, 3300, 3300, 3400, 4000, 4600, 4400, 2600, 2200, 3600, 3800, 2400, 1500, 1100, 3100, 3200, 1800, 1800, 800, 2100, 2500, 2800, 1300, 900, 0, 1400, 2000, 2500, 4000, 3300, 2100, 2900],
[5300, 5400, 4300, 4500, 3700, 4700, 4700, 4400, 2600, 3200, 3000, 4000, 3600, 2200, 2400, 3800, 2900, 2500, 1700, 1800, 3200, 3200, 2200, 700, 1100, 1400, 2700, 2300, 1400, 0, 600, 1100, 5400, 1900, 3500, 1500],
[5800, 5500, 4400, 3900, 3100, 5300, 5300, 4500, 2700, 2600, 2400, 4600, 4200, 1600, 1800, 4400, 3500, 3100, 1100, 1200, 3800, 3800, 2800, 1300, 500, 800, 3300, 2900, 2000, 600, 0, 500, 6000, 2000, 4100, 1600],
[5300, 5000, 3900, 3400, 2600, 5800, 5800, 4700, 2900, 2800, 1900, 5100, 4700, 1800, 1300, 4900, 4000, 3600, 1300, 700, 4300, 4300, 3300, 1800, 1000, 300, 3800, 3400, 2500, 1100, 500, 0, 5900, 2200, 4400, 1800],
[600, 900, 2000, 2500, 3300, 700, 1200, 2400, 3700, 4500, 4000, 1400, 1800, 5100, 4600, 1900, 2500, 2900, 5300, 5200, 3000, 3300, 3100, 5200, 5900, 5600, 3500, 3900, 3900, 5300, 5900, 5900, 0, 4400, 2900, 4800],
[3800, 3500, 2400, 2900, 3000, 4200, 3700, 2500, 700, 1500, 2300, 3700, 3300, 700, 1700, 4200, 3600, 3200, 900, 1500, 4700, 4400, 3300, 1200, 1500, 1900, 4600, 4200, 3300, 1900, 2000, 2200, 4400, 0, 2200, 400],
[2800, 2800, 3900, 4400, 5200, 2200, 2200, 1300, 2900, 3700, 4500, 1500, 1100, 2900, 3900, 2000, 1400, 1000, 3100, 3700, 2700, 2400, 1300, 3400, 3700, 4100, 3200, 3000, 2100, 3500, 4100, 4400, 2900, 2200, 0, 2600],
[4200, 3900, 2800, 3300, 3000, 4600, 4100, 2900, 1100, 1900, 2300, 4100, 3700, 1000, 1700, 4500, 3600, 3200, 500, 1100, 4300, 4000, 2900, 800, 1100, 1500, 4200, 3800, 2900, 1500, 1600, 1800, 4800, 400, 2600, 0]
]
demands = [0, 0, 0, 5, 6, 6, 5, 2, 3, 3, 6, 4, 3, 6, 2, 7, 4, 2, 3, 0, 5, 3, 8, 3, 6, 0, 3, 4, 2, 1, 5, 0, 0, 0, 0, 0]

num_vehicles, depot = 12, 33


# RoutingIndexManager 的参数为 位置的数目，车辆数量，起始位置
manager = pywrapcp.RoutingIndexManager(
    len(distance_matrix), num_vehicles, depot)

# 创建路由模型
routing = pywrapcp.RoutingModel(manager)

# 创建距离回调函数
transit_callback_index = routing.RegisterTransitCallback(
    lambda i, j: distance_matrix[manager.IndexToNode(i)][manager.IndexToNode(j)])

# 对所有车辆设置两点之间的运输成本计算函数
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# 添加容量维度的约束
demand_callback_index = routing.RegisterUnaryTransitCallback(
    lambda i: demands[manager.IndexToNode(i)])
routing.AddDimensionWithVehicleCapacity(
    demand_callback_index, 0, [10]*12, True, 'Capacity')

# 设置默认的搜索参数和用于寻找第一个解决方案的启发式方法
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
# 设置本地化的启发式搜索方法
search_parameters.local_search_metaheuristic = (
    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
# 设置最大计算时长
search_parameters.time_limit.FromSeconds(1)

# 开始计算
solution = routing.SolveWithParameters(search_parameters)

# 获取目标值
print("目标值：", solution.ObjectiveValue())
max_route_distance = 0
route_distances = []
total_load = 0
for vehicle_id in range(num_vehicles):
    index = routing.Start(vehicle_id)
    print(f"第{vehicle_id}号车")
    route_distance, route_load = 0, 0
    route_loads = [(manager.IndexToNode(index), 0)]
    while not routing.IsEnd(index):
        route_load += demands[manager.IndexToNode(index)]
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_loads.append((manager.IndexToNode(index), route_load))
        route_distance += routing.GetArcCostForVehicle(
            previous_index, index, vehicle_id)
    route_distances.append(route_distance)
    max_route_distance = max(route_distance, max_route_distance)
    total_load += route_load
    print(" -> ".join(map(str, route_loads)))
    print("运行距离：", route_distance)
    print()
print(
    f"最长路线的距离：{max_route_distance} m，总距离：{sum(route_distances)} m，总承重：{total_load}")

# 创建有向图
G = nx.DiGraph()

# 添加节点
for i in range(len(distance_matrix)):
    G.add_node(i)

# 添加边
for vehicle_id in range(num_vehicles):
    index = routing.Start(vehicle_id)
    while not routing.IsEnd(index):
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        G.add_edge(manager.IndexToNode(previous_index), manager.IndexToNode(index))

# 绘制图形
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=12, arrows=True)

# 显示图形
plt.axis('off')
plt.show()