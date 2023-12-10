from utils import utils
from collections import defaultdict
from dataclasses import dataclass, field
from math import lcm


class Node:
    def __init__(self, origin: str) -> None:
        self.origin: str = origin
        self.left = None
        self.right = None

        self.in_degree: int = 0
        self.out_degree: int = 0

    def connect(self, left=None, right=None):
        if left:
            self.left = left
            self.left.in_degree += 1
            self.out_degree += 1
        if right:
            self.right = right
            self.right.in_degree += 1
            self.out_degree += 1

    def __hash__(self) -> int:
        return hash(self.origin)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, str):
            return self.origin == __value
        return self.origin == __value.origin

    def __repr__(self) -> str:
        left = "" if not self.left else self.left.origin
        right = "" if not self.right else self.right.origin
        return f"{self.origin} --> [{left}, {right}] | in: {self.in_degree} out: {self.out_degree}"

    def __str__(self) -> str:
        return self.__repr__()


@dataclass(eq=False)
class Graph:
    nodes: dict[str, Node] = field(default_factory=dict)

    def add_map(self, origin: str, left: str, right: str) -> None:
        # Don't add self cycles to the graph
        if left != origin and right != origin:
            origin_node: Node = self.nodes.get(origin, Node(origin))
            self.nodes[origin] = origin_node

            left_node: Node = self.nodes.get(left, Node(left))
            origin_node.connect(left=left_node)
            self.nodes[left] = origin_node.left

            right_node: Node = self.nodes.get(right, Node(right))
            origin_node.connect(right=right_node)
            self.nodes[right] = origin_node.right

    def traverse(
        self,
        instructions: str,
        exhaust_instruction: bool = False,
        source: str = "AAA",
        source_token: str = 'A',
        target: str = "ZZZ",
        target_token: str = 'Z',
        max_iter: int = 100_000,
    ) -> Node:
        
        steps: int = 0
        iter_count: int = 0
        instruction_index: int = 0
        
        if not exhaust_instruction:
            current_node: Node = self.nodes[source]

            while current_node and current_node != target and iter_count < max_iter:
                current_instruction: str = instructions[instruction_index]
                if current_instruction == "L":
                    current_node = current_node.left
                else:
                    current_node = current_node.right

                instruction_index = (instruction_index + 1) % len(instructions)

                iter_count += 1
                steps += 1
        else:
            current_nodes: list[Node] = [node[1] for node in self.nodes.items() if node[0].endswith(source_token)]
            step_counts: list[int] = [0] * len(current_nodes)
            arrived: list[bool] = [False] * len(current_nodes)

            while not all(arrived) and iter_count < max_iter:
                
                for i in range(len(current_nodes)):
                    if not arrived[i]:
                        step_counts[i] += 1
                    else:
                        continue

                    if instructions[instruction_index] == 'L':    
                        current_nodes[i] = current_nodes[i].left
                    else:
                        current_nodes[i] = current_nodes[i].right
                    
                    if current_nodes[i].origin.endswith(target_token):
                        arrived[i] = True
                    
                instruction_index = (instruction_index + 1) % len(instructions)
                iter_count += 1

            steps = lcm(*step_counts)
        return steps

    def __repr__(self) -> str:
        node_list = sorted(list(self.nodes.items()), key=lambda node: node[1].origin)
        return "\n".join(str(node[1]) for node in node_list)


def parse_lines(lines: list[str]) -> tuple[list[str], Graph]:
    instructions: list[str] = lines[0]

    # network: dict[str, list[tuple[str]]] = defaultdict(list)
    graph = Graph()
    for line in lines[2:]:
        node_from, node_to_raw = line.split(" = ")
        left_node, right_node = node_to_raw[1:4], node_to_raw[-4:-1]
        graph.add_map(node_from, left_node, right_node)

    return instructions, graph

if __name__ == "__main__":
    test: bool = False
    lines: [str] = utils.read_lines("day_8-data.txt", test=test)

    instructions_part_1, graph_part_1 = parse_lines(lines)
    iter_count_part_1: int = graph_part_1.traverse(instructions_part_1)
    print(f"{iter_count_part_1=}")

    instructions_part_2, graph_part_2 = parse_lines(lines)
    iter_count_part_2: int = graph_part_2.traverse(instructions_part_2, exhaust_instruction=True)
    print(f"{iter_count_part_2=}")

