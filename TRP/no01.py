from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

distance_matrix = [
    [0, 451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 293, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 293, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 50],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 50, 0],
]
n = len(distance_matrix)
# RoutingIndexManager 的参数为 位置的数目，车辆数量，起始位置
manager = pywrapcp.RoutingIndexManager(n, 1, 0)
# 创建路由模型
routing = pywrapcp.RoutingModel(manager)

# 创建距离回调函数
transit_callback_index = routing.RegisterTransitCallback(
    lambda i, j: distance_matrix[i % n][j % n])
# 设置两点之间的运输成本计算方法
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
# 设置默认的搜索参数和用于寻找第一个解决方案的启发式方法:
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
# 计算并获取最短距离
solution = routing.SolveWithParameters(search_parameters)
print("最短距离：", solution.ObjectiveValue())
# 保存最短路径
index = routing.Start(0)
route = [manager.IndexToNode(index)]
while not routing.IsEnd(index):
    index = solution.Value(routing.NextVar(index))
    route.append(index % n)
print(" -> ".join(map(str, route)))
