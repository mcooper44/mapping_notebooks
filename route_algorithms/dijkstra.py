from heapq import heapify, heappop, heappush


class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph


    def add_edge(self, node1, node2, weight):
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = weight


    def shortest_distances(self, source: str):
        distances = {node: float('inf') for node in self.graph}
        distances[source] = 0


        priority_q = [(0, source)]
        heapify(priority_q)

        visited = set()

        while priority_q:
            current_distance, current_node = heappop(priority_q)

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbour, weight in self.graph[current_node].items():
                tentative_distance = current_distance + weight
                if tentative_distance < distances[neighbour]:
                    distances[neighbour] = tentative_distance
                    heappush(priority_q, (tentative_distance, neighbour))

        predecessors = {node: None for node in self.graph}

        for node, distance in distances.items():
            for neighbour, weight in self.graph[node].items():
                if distances[neighbour] == distance + weight:
                    predecessors[neighbour] = node

        return distances, predecessors

    def shortest_path(self, source: str, target: str):
        _, predecessors = self.shortest_distances(source)

        path = []
        current_node = target

        while current_node:
            path.append(current_node)
            current_node = predecessors[current_node]

        path.reverse()
        return path


def main():
    wg = {'A': {'B': 3, 'C': 3},
         'B': {'A': 3, 'D': 3.5, 'E': 2.8},
         'C': {'A': 3, 'E': 2.8, 'F': 3.5},
         'D': {'B': 3.5, 'E': 3.1, 'G': 10},
         'E': {'B': 2.8, 'C': 2.8, 'D': 3.1, 'G': 7},
         'F': {'G': 2.5, 'C': 3.5},
         'G': {'F': 2.5, 'E': 7, 'D': 10}}

    g = Graph(wg)
    print(g.shortest_path('B', 'F'))
    print(g.shortest_path('A', 'G'))

main()

