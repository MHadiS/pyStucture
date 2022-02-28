from pyStack import Stack
from pyQueue import Queue


__version__ = 1


class Graph:
    """a class for saving graph and give you graph data structure
    """

    def __init__(self, v: set, e: set, graph_type: str):
        """Define needed variables for other methods

        Args:
            v (set): A set of graph vertices
            e (set): A set of graph edges
            graph_type (str): A string for defining the graph types

        Raises:
            ValueError: If you give wrong type to the class this error raise with 'Unknown type of graph' message

        Description:
            v set should be like this: NAME = {2, 1, 3, 4, ....}
            e set should be like this: NAME = {(1, 2), (2, 3), (3, 4), (4, 1), ....}
            graph_types include:
                D : Directed graph
                UD : UnDirected graph
            weight of an edge by default is 1, but you can change it like this: A = (1, 2, 3)
            now A edge connect vertex 1 to vertex 2 with weight 3
        """
        self.V = v
        self.E = e
        self.i = 0  # ignore this
        self.type = graph_type
        self.p = len(v)
        self.q = len(e)

        # check the graph type
        if graph_type.lower() in ("ud", "d"):
            self.type = graph_type.lower()
        else:
            raise ValueError("Unknown type of graph")

        if self.q == 0:
            self.empty = True
        else:
            self.empty = False

        # check graph has cycles or not
        scc = self.cycles()
        array = [scc[key] for key in scc]
        array.sort()
        has_cycle = None
        for index in range(1, len(array)):
            value1 = array[index - 1]
            value2 = array[index]
            if value1 == value2:
                has_cycle = True

        # self.DAG be True when the graph is Directed Acyclic Graph
        self.DAG = (self.type == "d") and not has_cycle

    def out_deg(self, vertex: int):
        """return the out-degree of a vertex

        Args:
            vertex (int): vertex number in v set

        Returns:
            vertex degree: vertex degree is number of edges connected to a vertex
        """
        d = 0
        if self.type == "d":
            for edge in self.E:
                if (vertex in edge) and (edge.index(vertex) == 0):
                    d += 1
        else:
            for edge in self.E:
                if vertex in edge:
                    d += 1
                    if edge[0] == edge[1]:
                        d += 1
        return d

    def in_deg(self, vertex: int):
        """return the in-degree of a vertex

        Args:
            vertex (int): vertex number in v set

        Returns:
            vertex degree: vertex degree is number of edges connected to a vertex
        """
        d = 0
        if self.type == "d":
            for edge in self.E:
                if (vertex in edge) and (edge.index(vertex) == 1):
                    d += 1
        else:
            for edge in self.E:
                if vertex in edge:
                    d += 1
                    if edge[0] == edge[1]:
                        d += 1
        return d

    def neighboring_vertices(self, vertex: int):
        """return neighbors of a vertex

        Args:
            vertex (int): vertex number in v set

        Returns:
            list: a list of neighboring vertices of the vertex 
        """
        neighbors = []

        # finding vertex neighbors of a directed graph
        if self.type == "d":
            for edge in self.E:
                formatted_edge = (edge[0], edge[1])
                if vertex in formatted_edge:
                    i = formatted_edge.index(vertex)
                    if i == 0:
                        neighbors.append(edge[1])

        # finding vertex neighbors of an undirected graph
        elif self.type == "ud":
            for edge in self.E:
                formatted_edge = (edge[0], edge[1])
                if vertex in formatted_edge:
                    i = 1 - formatted_edge.index(vertex)
                    neighbors.append(formatted_edge[i])

        return neighbors

    def add_edge(self, edge: tuple):
        """add an edge to e set

        Args:
            edge (tuple): the new edge

        Raises:
            NameError: if the vertices wasn't in v this error will raise
        """
        is_valid = True
        for v in edge:
            if not(v in self.V):
                is_valid = False
        if is_valid:
            self.E.add(edge)
        else:
            raise NameError("Undefined vertex")

    def add_vertex(self, vertex: int):
        """add a new vertex to v set

        Args:
            vertex (int): new vertex
        """
        self.V.add(vertex)

    def adjacency_list(self):
        """make adjacency list of the graph and return it

        Returns:
            dict: adjacency list of the graph
        """
        adjacency_list = dict.fromkeys(self.V, None)
        for vertex in self.V:
            neighbors = self.neighboring_vertices(vertex)
            adjacency_list[vertex] = neighbors
        return adjacency_list

    def has_path(self, start: int, target: int):
        """check there is a path between start and target vertex using DFS.
            algorithm time complexity = O(V + E)
            algorithm space complexity = O(V)

        Args:
            start (int): starting vertex
            target (int): ending vertex

        Returns:
            boolean: a boolean value to show there is a path or not
        """
        visited = []
        stack = Stack()
        stack.put(start)
        target_found = False
        while not target_found:
            if stack.length == 0:
                break
            vertex = stack.get()
            if not(vertex in visited):
                if vertex == target:
                    target_found = True
                else:
                    visited.append(vertex)
                    for v in self.neighboring_vertices(vertex):
                        stack.put(v)
        return target_found

    def dijkstra(self, start: int):
        """A SSSP dijkstra to find the shortest path
            algorithm time complexity = O(V ^ 2)
            algorithm space complexity = O(V)
            WARNING : This algorithm won't work for negative edge weight


        Args:
            start (int): the source vertex

        Returns:
            dict: the distance dict in dijkstra algorithm
        """
        data = {v: {"dist": float("inf"), "prev": None} for v in self.V}
        data[start]["dist"] = 0
        pq = {start: 0}
        visited = []
        while True:
            if len(pq) == 0:
                return data
            min_ = float("inf")
            vertex = None
            for v in pq:
                if pq[v] < min_:
                    min_ = pq[v]
                    vertex = v
            pq.pop(vertex)
            visited.append(vertex)
            for n in self.neighboring_vertices(vertex):
                if not(n in visited):
                    new_dist = self.weight((vertex, n)) + data[vertex]["dist"]
                    if new_dist < data[n]["dist"]:
                        data[n]["dist"] = new_dist
                        pq[n] = new_dist
                        data[n]["prev"] = vertex

    def shortest_path(self, start: int, target: int):
        """finding the shortest path between to vertex with dijkstra method

        Args:
            start (int): the source vertex
            target (int): the end vertex

        Returns:
            list: a list that has the shortest path
        """
        path = [target]
        result = self.dijkstra(start)
        vertex = result[target]["prev"]
        while vertex is not None:
            path.insert(0, vertex)
            vertex = result[vertex]["prev"]
        return path

    def maximum(self, deg_type: str = "OD"):
        """find the vertex with the biggest in or out degree

        Args:
            deg_type (str, optional): ID means you want biggest in degree. OD means you want biggest out degree. Defaults to "OD".

        Returns:
            dict: this dict includes vertex number in V set and its degree
        """
        degrees = None
        if deg_type.lower() == "od":
            degrees = [self.out_deg(v) for v in self.V]
        if deg_type.lower() == "id":
            degrees = [self.in_deg(v) for v in self.V]
        degree = max(degrees)
        vertex = tuple(self.V)[degrees.index(degree)]
        return {"vertex": vertex, "degree": degree}

    def minimum(self, deg_type="OD"):
        """find the vertex with the smallest in or out degree

        Args:
            deg_type (str, optional): ID means you want smallest in degree. OD means you want smallest out degree. Defaults to "OD".

        Returns:
            dict: this dict includes vertex number in V set and its degree
        """
        degrees = None
        if deg_type.lower() == "od":
            degrees = [self.out_deg(v) for v in self.V]
        if deg_type.lower() == "id":
            degrees = [self.in_deg(v) for v in self.V]
        degree = min(degrees)
        vertex = tuple(self.V)[degrees.index(degree)]
        return {"vertex": vertex, "degree": degree}

    def weight(self, edge: tuple):
        """find the weight of an edge

        Args:
            edge (tuple): the edge tuple in e set.

        Returns:
            int: return the weight of the edge
        """
        for e in self.E:
            formatted_edge = (e[0], e[1])
            if formatted_edge == edge:
                try:
                    return e[2]
                except IndexError:
                    return 1

    def colorize(self):
        """colorize a graph. each vertex has different color with its neighbors.
            this algorithm use minimum colors to colorize graph.

        Returns:
            dict: a dict of vertices with their color
        """
        i = 0
        colors = {i}
        colored_vertices = dict.fromkeys(self.V, None)
        for vertex in self.V:
            neighbors_colors = set()
            for n in self.neighboring_vertices(vertex):
                color = colored_vertices[n]
                if not(color is None):
                    neighbors_colors.add(color)
            new_color = colors - neighbors_colors
            if new_color == set():
                i += 1
                colors.add(i)
                colored_vertices[vertex] = i
            else:
                colored_vertices[vertex] = new_color.pop()
        return colored_vertices

    def minimum_colors(self):
        """use colorize method to find minimum colors needed for colorize the graph

        Returns:
            int: number of minimum colors needed for colorize the graph
        """
        colored_graph = self.colorize()
        colors = set()
        for key in colored_graph:
            colors.add(colored_graph[key])
        return len(colors)

    def cycles(self):
        UNVISITED = -1
        ids = dict.fromkeys(self.V, UNVISITED)
        low_link = ids.copy()
        stack = Stack()
        for vertex in self.V:
            if ids[vertex] == UNVISITED:
                result = self.tarjan_dfs(vertex, stack, ids, low_link, self.i)
                ids = result[0]
                low_link = result[1]
        low_link.pop(None)
        return low_link

    def tarjan_dfs(self, vertex, stack, ids, low_link, i):
        stack.put(vertex)
        ids[vertex] = self.i
        low_link[vertex] = self.i
        self.i += 1
        for n in self.neighboring_vertices(vertex):
            if ids[n] == -1:
                self.tarjan_dfs(n, stack, ids, low_link, i)

            if stack.count(n) != 0:
                low_link[vertex] = min(low_link[n], low_link[vertex])

        if low_link[vertex] == ids[vertex]:
            for j in range(stack.length):
                v = stack.pop()
                low_link[v] = low_link[vertex]
                if v == vertex:
                    break
            return ids, low_link

    def topsort(self):
        """find the topological order of the graph with Kahn's algorithms
            algorithm time complexity = O(V + E)
            algorithm space complexity = O(V)

        Raises:
            TypeError: none directed acyclic graphs don't have topological order

        Returns:
            list: a list of the graph's topological order
        """
        if not self.DAG:
            raise TypeError("your graph isn't directed acyclic graph")
        order = []
        queue = Queue()
        in_degrees = {v: self.in_deg(v) for v in self.V}
        for vertex in in_degrees:
            if in_degrees[vertex] == 0:
                queue.put(vertex)

        while not queue.is_empty():
            element = queue.get()
            order.append(element)
            for n in self.neighboring_vertices(element):
                in_degrees[n] = in_degrees[n] - 1
            del in_degrees[element]

            for vertex in in_degrees:
                if in_degrees[vertex] == queue.count(vertex) == 0:
                    queue.put(vertex)
        return order
