from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['locations'] = [0, 1, 2, 3, 4, 5, 6]  # 位置索引
    data['num_vehicles'] = 5  # 车辆数量
    data['depot'] = 0  # 仓库索引
    data['vehicle_capacities'] = [15]*5  # 车辆容量
    data['pickups_deliveries'] = [(1, 2, 5), (3, 4, 6)]  # (取货点,送货点,货物量)
    data['distance_matrix'] = [
        [0, 10, 20, 30, 40],
        [10, 0, 15, 25, 35],
        [20, 15, 0, 20, 30],
        [30, 25, 20, 0, 10],
        [40, 35, 30, 10, 0]
    ]  # 距离矩阵
    return data


def main():
    """Entry point of the program."""
    data = create_data_model()

    # 创建求解器实例
    manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'],
                                           data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # 定义Cost Callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 定义Demand Callback
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return sum(demand for pickup, delivery, demand in data['pickups_deliveries']
                   if pickup == from_node or delivery == from_node)

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # 添加Pickup and Delivery约束
    for pickup, delivery, _ in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(pickup)
        delivery_index = manager.NodeToIndex(delivery)
        routing.AddPickupAndDelivery(pickup_index, delivery_index)

    # 设置求解参数
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # 求解问题
    solution = routing.SolveWithParameters(search_parameters)

    # 打印结果
    if solution:
        print(f'Objective: {solution.ObjectiveValue()}')
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            while not routing.IsEnd(index):
                plan_output += ' {} -> '.format(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            plan_output += '{}\n'.format(manager.IndexToNode(index))
            print(plan_output)
    else:
        print('No solution found!')


if __name__ == '__main__':
    main()