class Node:
    def __init__(self, id: str, is_root=False):
        self.id = id
        self.is_root = is_root
        self.edges_in = []
        self.edges_out = []
        self.run_count = 0

    def increment_run_count(self):
        self.run_count += 1

    def __repr__(self) -> str:
        return f"Node(id={self.id}, edges_out={self.edges_out})"

    def is_root(self):
        return self.is_root

            
class Edge:
    def __init__(self, source: Node, destination: Node, weight: int = 1):
        self.source = source
        self.destination = destination
        self.weight = weight

    def __repr__(self) -> str:
        return f"Edge(destination={self.destination}, weight={self.weight})"


class Graph:
    def __init__(self):
        self.root = None
        self.nodes = {}

    def __repr__(self) -> str:
        return f"Graph(root={self.root})"

    def add_edge(self, src_id, dest_id, weight=1) -> None:
        src_node = self.add_node(src_id)
        dest_node = self.add_node(dest_id)
        edge = Edge(source=src_node, destination=dest_node, weight=weight)
        src_node.edges_out.append(edge)
        dest_node.edges_in.append(edge)

    def add_node(self, id: str, is_root=False) -> Node:
        if id not in self.nodes:
            if is_root:
                if self.root:
                    raise ValueError("There can be only one root node.")
                self.root = Node(id, is_root=True)
                self.nodes[id] = self.root
            else:
                self.nodes[id] = Node(id)
        return self.nodes[id]

    def get_node(self, id: str) -> Node:
        return self.nodes.get(id)

    def find_loop(self) -> Node:
        """If there is a loop in the graph, return where it originates from."""

        # use a input set to keep track of visited nodes.  if any destination edges are already 
        # in the set, we have a loop
        visited = set()
        def find_loop(node):
            if node in visited:
                return node
            visited.add(node)
            for edge in node.edges_out:
                if find_loop(edge.destination):
                    return edge.destination
            visited.remove(node)
            return None
        return find_loop(self.root)
    