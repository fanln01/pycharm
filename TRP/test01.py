from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

distance_matrix = [
    [0, 548, 776, 696, 582, 274, 502, 194, 308,
        194, 536, 502, 388, 354, 468, 776, 662],
    [548, 0, 684, 308, 194, 502, 730, 354, 696,
        742, 1084, 594, 480, 674, 1016, 868, 1210],
    [776, 684, 0, 992, 878, 502, 274, 810, 468,
        742, 400, 1278, 1164, 1130, 788, 1552, 754],
    [696, 308, 992, 0, 114, 650, 878, 502, 844,
        890, 1232, 514, 628, 822, 1164, 560, 1358],
    [582, 194, 878, 114, 0, 536, 764, 388, 730,
        776, 1118, 400, 514, 708, 1050, 674, 1244],
    [274, 502, 502, 650, 536, 0, 228, 308, 194,
        240, 582, 776, 662, 628, 514, 1050, 708],
    [502, 730, 274, 878, 764, 228, 0, 536, 194,
        468, 354, 1004, 890, 856, 514, 1278, 480],
    [194, 354, 810, 502, 388, 308, 536, 0, 342,
        388, 730, 468, 354, 320, 662, 742, 856],
    [308, 696, 468, 844, 730, 194, 194, 342, 0,
        274, 388, 810, 696, 662, 320, 1084, 514],
    [194, 742, 742, 890, 776, 240, 468, 388, 274,
        0, 342, 536, 422, 388, 274, 810, 468],
    [536, 1084, 400, 1232, 1118, 582, 354, 730,
        388, 342, 0, 878, 764, 730, 388, 1152, 354],
    [502, 594, 1278, 514, 400, 776, 1004, 468,
        810, 536, 878, 0, 114, 308, 650, 274, 844],
    [388, 480, 1164, 628, 514, 662, 890, 354, 696,
        422, 764, 114, 0, 194, 536, 388, 730],
    [354, 674, 1130, 822, 708, 628, 856, 320, 662,
        388, 730, 308, 194, 0, 342, 422, 536],
    [468, 1016, 788, 1164, 1050, 514, 514, 662,
        320, 274, 388, 650, 536, 342, 0, 764, 194],
    [776, 868, 1552, 560, 674, 1050, 1278, 742,
        1084, 810, 1152, 274, 388, 422, 764, 0, 798],
    [662, 1210, 754, 1358, 1244, 708, 480, 856,
        514, 468, 354, 844, 730, 536, 194, 798, 0]
]
num_vehicles, depot = 4, 0
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

# 添加距离约束
dimension_name = 'Distance'
# 创建一个距离维度用于计算每辆车沿其路线行驶的累计距离
routing.AddDimension(transit_callback_index, 0, 3000, True, dimension_name)
distance_dimension = routing.GetDimensionOrDie(dimension_name)
# 设置全局跨度
distance_dimension.SetGlobalSpanCostCoefficient(100)

# 设置默认的搜索参数和用于寻找第一个解决方案的启发式方法:
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
# 开始计算
solution = routing.SolveWithParameters(search_parameters)
# 获取目标值
print("目标值：", solution.ObjectiveValue())
max_route_distance = 0
route_distances = []
for vehicle_id in range(num_vehicles):
    index = routing.Start(vehicle_id)
    print(f"第{vehicle_id}号车")
    route = [manager.IndexToNode(index)]
    route_distance = 0
    while not routing.IsEnd(index):
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        route_distance += routing.GetArcCostForVehicle(
            previous_index, index, vehicle_id)
    route_distances.append(route_distance)
    max_route_distance = max(route_distance, max_route_distance)
    print(" -> ".join(map(str, route)))
    print("运行距离：", route_distance)
print(f"最长路线的距离：{max_route_distance} m，总距离：{sum(route_distances)} m")
