from collections import deque
import math
import operator


class Problem:
    def __init__(self, knowledge, cost, edge, start_node, end_node):
        self.knowledge = knowledge
        self.cost = cost
        self.edge = edge
        self.start_node = start_node
        self.end_node = end_node

    # function for retrieving graph
    def get_map(self):
        return self.knowledge

    # function for retrieving cost at a node
    def get_costGraph(self):
        return self.cost

    # function for retrieving edge graph cost
    def get_edgeGraph(self):
        return self.edge

    # function for retrieving start_node
    def get_startNode(self):
        return self.start_node

    # function for retrieving end_node or goal
    def get_endNode(self):
        return self.end_node

    # action mapping function
    def actionFunc(self, node, actiontype):
        map = self.get_map()
        if node in map:
            ch_nodes = map[node]
            if actiontype == "turnLeft":
                return ch_nodes[0]
            elif actiontype == "goStraight":
                return ch_nodes[1]
            else:
                return ch_nodes[2]

    # Depth-First Search implementation
    def DFS(self, map, node, reached=None, result=None):

        if reached is None:
            reached = set()
        if result is None:
            result = []

        reached.add(node)
        result.append(node)

        if node == self.get_endNode():
            return result, True

        if node.get_action() is not None:
            for action in node.get_action():
                leafnode = self.actionFunc(node, action)
                leafnode.set_parent(node)

                if leafnode not in reached:
                    result_path, found = self.DFS(map, leafnode, reached, result)
                    if found:
                        return result_path, True

        return result, False

    # Breadth-First Search Implementation
    def BFS(self, map, node):

        reached = set()
        result = []
        queue = deque()

        reached.add(node)
        result.append(node)
        queue.append(node)

        while queue:
            node = queue.popleft()

            if node == self.get_endNode():
                return result, True

            if node.get_action() is not None:
                for action in node.get_action():
                    leafnode = self.actionFunc(node, action)

                    leafnode.set_parent(node)
                    if leafnode not in reached:
                        reached.add(leafnode)
                        queue.append(leafnode)
                        result.append(leafnode)

                    if leafnode == self.get_endNode():
                        return result, True

        return result, False

    def get_lowestCost(self, map, reached):

        cost_atNode = {}

        for x in map.keys():
            if x not in reached:
                cost_atNode[x] = x.get_cost()
        print(f"isi dari variabel cost at node: ")
        for key, value in cost_atNode.items():
            print(f"{key.get_state()} : {value}")

        if cost_atNode:
            node = min(cost_atNode.items(), key=operator.itemgetter(1))
            reached.add(node[0])
            print(f"isi dari node terkecil: {node[0].get_state()}")
            return node[0], reached
        else:
            return None, reached

    # implementing Djikstra algorithm
    def djikstra(self, map, node):

        edge = self.get_edgeGraph()
        reached = set()
        result = []

        node.set_cost(0)

        n_node, reached = self.get_lowestCost(map, reached)

        while n_node:

            if n_node.get_action() is not None:
                for action in n_node.get_action():
                    leafnode = self.actionFunc(n_node, action)
                    print(
                        f"child node dari {n_node.get_state()} adalah {leafnode.get_state()}"
                    )
                    cost_leafnode = edge[n_node][leafnode]
                    print(
                        f"cost dari child node saat ini adalah: {cost_leafnode}, cost dari induk: {n_node.get_cost()}"
                    )

                    if cost_leafnode + n_node.get_cost() <= leafnode.get_cost():
                        leafnode.set_cost(cost_leafnode + n_node.get_cost())
                        print(f"cost baru dari leafnode adalah {leafnode.get_cost()}")
                        leafnode.set_parent(n_node)

            n_node, reached = self.get_lowestCost(map, reached)
            if n_node == self.get_endNode():
                return reached, True

        return reached, False

    # Retrieving list of neighbor nodes
    def get_ChildNodes(self, method):
        map = self.get_map()
        start_node = self.get_startNode()
        if method == "DFS":
            result, status = self.DFS(map, start_node)
        elif method == "BFS":
            result, status = self.BFS(map, start_node)
        else:
            result, status = self.djikstra(map, start_node)
            if self.get_endNode() in result:
                result = self.get_endNode()
            else:
                status = False

        return result, status


class Node:
    def __init__(self, state, action):
        self.state = state
        self.action = action
        self.parent = None
        self.cost = math.inf

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def set_parent(self, node):
        self.parent = node

    def get_action(self):
        return self.action

    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost


def solution(node):
    print(node.get_state())
    if node.get_parent() is not None:
        solution(node.get_parent())
    else:
        return node.get_state()


def main():
    # creating nodes with its state and actions
    node_0 = Node("A", ["turnLeft", "goStraight"])
    node_1 = Node("B", ["turnLeft", "goStraight", "turnRight"])
    node_2 = Node("C", ["turnLeft", "goStraight"])
    node_3 = Node("D", None)
    node_4 = Node("E", None)
    node_5 = Node("F", None)
    node_6 = Node("G", None)

    # mapping
    knowledge = {
        node_0: [node_1, node_2],
        node_1: [node_3, node_4, node_5],
        node_2: [node_5, node_6],
        node_3: None,
        node_4: None,
        node_5: None,
        node_6: None,
    }

    # cost at node
    cost = {
        node_0: math.inf,
        node_1: math.inf,
        node_2: math.inf,
        node_3: math.inf,
        node_4: math.inf,
        node_5: math.inf,
        node_6: math.inf,
    }
    # edge cost
    edge = {
        node_0: {node_1: 6, node_2: 5},
        node_1: {node_3: 4, node_4: 6, node_5: 6},
        node_2: {node_5: 4, node_6: 7},
        node_3: None,
        node_4: None,
        node_5: None,
        node_6: None,
    }

    pathFinding = Problem(knowledge, cost, edge, start_node=node_0, end_node=node_5)

    path_list, status = pathFinding.get_ChildNodes(method="Djikstra")

    if status:
        print(f"Jalur terdekat menuju {pathFinding.get_endNode().get_state()} adalah: ")
        solution(path_list)
    else:
        print("No target found!")


if __name__ == "__main__":
    main()
