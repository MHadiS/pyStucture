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
            graph_type (str): A string for defining the graphs type

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

    def is_DAG(self):
        """check is graph directed acyclic graph or not

        Returns:
            boolean: if output is true means the graph is directed acyclic and if it is false the graph isn't directed acyclic

        Description:
            when a graph is directed and doesn't have any cycles we call it a directed acyclic graph
        """

        # check graph has cycles or not
        scc = self.cycles()
        has_cycle = False
        for c in scc:
            if len(c) != 1:
                has_cycle = True
                break
        return (self.type == "d") and not has_cycle

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
        looked = []
        stack = Stack()
        stack.put(start)
        target_found = False
        while not target_found:
            if stack.length == 0:
                break
            vertex = stack.get()
            if not(vertex in looked):
                if vertex == target:
                    target_found = True
                else:
                    looked.append(vertex)
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
        """find the vertex with the biggest in-degree or out-degree

        Args:
            deg_type (str): ID means you want biggest in-degree. OD means you want biggest out-degree. Defaults to "OD".

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
        """find the vertex with the smallest in-degree or out-degree

        Args:
            deg_type (str): ID means you want smallest in-degree. OD means you want smallest out-degree. Defaults to "OD".

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
        """find the weight( or we can call it length) of an edge

        Args:
            edge (tuple): the edge tuple in e set.

        Returns:
            int: return the weight of the edge
        """
        for e in self.E:
            formatted_edge = (e[0], e[1])
            if formatted_edge == edge or formatted_edge == (edge[1], edge[0]):
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

    def reverse_edges(self):
        """revese the direction of edges

        Returns:
            set: reversed edges set
        """
        reversed_edges = set()
        for e in self.E:
            reversed_edge = (e[1], e[0])
            reversed_edges.add(reversed_edge)
        return reversed_edges

    def cycles(self):
        """find the SCC (Strongly Connected Components) of the graph with kosaraju's algorithm
            algorithm time complexity = O(V + E)
            algorithm space complexity = O(V)

        Returns:
            list: a 2D list of SCC
        """
        checked = []
        start = self.maximum()["vertex"]
        order_stack = self.dfs(start)
        print("checked = ", checked)
        self.E = self.reverse_edges()
        sccs = []
        for i in range(order_stack.length):
            vetrex = order_stack.pop()
            if not(vetrex in checked):
                scc = self.dfs(vetrex, checked, Stack())
                scc_list = []
                order_stack.show()
                for j in range(scc.length):
                    scc_list.append(scc.pop())
                sccs.append(scc_list)
        self.E = self.reverse_edges()
        return sccs

    def dfs(self, vertex: int, explored=[], order=Stack()):
        """explore the graph and return the order of visiting with DFS.
            algorithm time complexity = O(V + E)
            algorithm space complexity = O(V)


        Args:
            vertex (int): the start vertex of exploring
            explored (list): a list for saving explored vertices. Defaults to [].
            order (Stack): order of exploring vertices. Defaults to Stack().

        Returns:
            Stack: a stack of DFS visiting order
        """
        explored.append(vertex)
        print(vertex, explored, sep="\n")
        for n in self.neighboring_vertices(vertex):
            if not(n in explored):
                self.dfs(n, explored, order)
        order.push(vertex)
        return order

    def bfs(self, vertex: int):
        """explore the graph and return the order of visiting with BFS
            algorithm time complexity = O(V + E)
            algorithm space complexity = O(V)

        Args:
            vertex (int): start vertex

        Returns:
            list: a list of BFS visiting order
        """
        bfs_order = []
        q = Queue()
        q.put(vertex)

        while not q.is_empty():
            vertex = q.get()
            # check is vertex visited or not for don't visit visited vertices
            if not(vertex in bfs_order):
                bfs_order.append(vertex)
                for n in self.neighboring_vertices(vertex):
                    q.put(n)
        return bfs_order

    def topsort(self):
        """find the topological order of the graph with Kahn's algorithms
            algorithm time complexity = O(V + E)
            algorithm space complexity = O(V)

        Raises:
            TypeError: none directed acyclic graphs don't have topological order

        Returns:
            list: a list of the graph's topological order
        """
        if not self.is_DAG():
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
