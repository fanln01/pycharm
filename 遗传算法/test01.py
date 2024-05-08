class Robot:
    def __init__(self, data, edges, load_capacity=10):
        self.data = {node[0]: (node[1], node[2]) for node in data}
        self.edges = {(edge[0], edge[1]): edge[2] for edge in edges}
        self.load_capacity = load_capacity
        self.sequences = []

    def dfs(self, node, visited, sequence, load):
        if node not in visited:
            visited.add(node)
            load += self.data[node][1] - self.data[node][0]
            sequence.append(node)

            if load == 0:
                self.sequences.append(sequence[:])
                return

            for next_node in self.get_neighbors(node):
                if next_node not in visited and load > 0:
                    self.dfs(next_node, visited, sequence, load)
                    visited.remove(next_node)
                    sequence.pop()
                    load -= self.data[next_node][1] - self.data[next_node][0]

    def get_neighbors(self, node):
        return [edge[1] for edge in self.edges if edge[0] == node]

    def find_shortest_path(self, start, end, visited=None):
        if visited is None:
            visited = set()
        if start == end:
            return [start]
        visited.add(start)
        shortest_path = None
        for neighbor in self.get_neighbors(start):
            if neighbor not in visited:
                path = self.find_shortest_path(neighbor, end, visited)
                if path:
                    if not shortest_path or len(path) < len(shortest_path):
                        shortest_path = [start] + path
        visited.remove(start)
        return shortest_path

    def generate_sequences(self):
        while any(data[1] > 0 for data in self.data.values()):
            visited = set()
            sequence = []
            load = self.load_capacity
            self.dfs(33, visited, sequence, load)

            for seq in self.sequences:
                start, end = seq[0], seq[-1]
                shortest_path = self.find_shortest_path(end, start)
                if shortest_path:
                    self.sequences.append(shortest_path)

        flattened_sequences = [node for seq in self.sequences for node in seq]
        return flattened_sequences

# 节点数据
data = [
    (1, 3, 0), (2, 4, 1), (3, 2, 0), (4, 5, 2), (5, 6, 0), (6, 6, 2), (7, 5, 0), (8, 2, 0), (9, 4, 0), (10, 3, 1),
    (11, 6, 0), (12, 4, 3), (13, 3, 0), (14, 6, 0), (15, 2, 0), (16, 7, 2), (17, 4, 0), (18, 2, 3), (19, 5, 0), (20, 6, 0),
    (21, 5, 2), (22, 3, 0), (23, 8, 0), (24, 3, 0), (25, 6, 2), (26, 2, 0), (27, 3, 0), (28, 4, 0), (29, 2, 2), (30, 1, 0),
    (31, 5, 0),(32, 0, 0), (33, 0, 0), (34, 0, 0), (35, 0, 0), (36, 0, 0)
]

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

# 创建机器人实例并生成访问序列
robot = Robot(data, edges)
access_sequence = robot.generate_sequences()
print(access_sequence)