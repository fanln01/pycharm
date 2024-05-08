import random

def generate_possible_sequences():
    # 节点相邻关系
    adjacency_map = {
        1: [5, 4],
        2: [4, 9],
        3: [9, 10],
        4: [1, 2, 7],
        5: [1, 6],
        6: [5],
        7: [4, 10],
        8: [10],
        9: [2, 3],
        10: [7, 8, 3]
    }

    # 生成可能的遍历顺序数组
    possible_sequences = []

    for _ in range(10):  # 生成10个可能的遍历顺序
        sequence = [1]  # 起始节点为1
        current_node = 1
        energy = 10  # 初始体力为10

        while len(sequence) < 10:  # 直到遍历到所有节点为止
            next_nodes = adjacency_map[current_node]

            # 过滤掉已经遍历过的节点
            next_nodes = [node for node in next_nodes if node not in sequence]

            if not next_nodes:  # 如果当前节点的相邻节点都已经遍历过，直接跳到节点10
                sequence.append(10)
                break

            next_node = random.choice(next_nodes)  # 从当前节点的相邻节点中随机选择一个
            sequence.append(next_node)

            # 根据节点与消耗体力的关系更新体力值
            if next_node in [1, 2, 3]:
                energy -= 1
            elif next_node in [4, 5, 6]:
                energy -= 2
            else:
                energy -= 3

            if energy <= 0:  # 如果体力为0，直接跳到节点10
                sequence.append(10)
                break

            current_node = next_node

        possible_sequences.append(sequence)

    return possible_sequences

# 测试函数
sequences = generate_possible_sequences()
for idx, sequence in enumerate(sequences):
    print(f"{idx+1}. {sequence}")
