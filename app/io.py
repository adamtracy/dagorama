from graphviz import Digraph
import json
import logging
import os

from app import INPUT_DIR, OUTPUT_DIR
from app.model import Graph


class NoRootError(Exception):
    pass


class MoreThanOneRootError(Exception):
    pass


class OrphanNodeError(Exception):
    pass


def parse_graph(raw_data: dict) -> Graph:
    graph = Graph()
    for node_id, node_data in raw_data.items():
        node = graph.get_node(node_id)
        if not node:
            node = graph.add_node(node_id, is_root=node_data.get("start", False))
        else:
            is_root = node_data.get("start", False)
            if is_root:
                if graph.root:
                    raise MoreThanOneRootError("There can be only one root node.")
                graph.root = node
                node.is_root = True
        for dest_id, weight in node_data.get("edges", {}).items():
            graph.add_edge(node_id, dest_id, weight)
        if not graph.root:
            raise NoRootError("There must be a root node.")
        for node in graph.nodes.values():
            if not node.is_root and not node.edges_in:
                raise OrphanNodeError(f"Node {node.id} has no incoming edges.")
    return graph


def viz_dag(graph: Graph, file_name) -> None:
    dot = Digraph(comment=f"DAG {file_name}")
    for node in graph.nodes.values():
        dot.node(node.id, node.id)
        for edge in node.edges_out:
            edge_color = "black"
            dot.edge(
                node.id, edge.destination.id, label=str(edge.weight), color=edge_color
            )

    output_file = os.path.join(OUTPUT_DIR, f"{file_name}")
    logging.info(f"Saving visualization to {output_file}.png")
    dot.render(output_file, format="png", cleanup=True)


def viz_graphs() -> None:
    # just render input data
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".json"):
            try:
                with open(os.path.join(INPUT_DIR, file_name), "r") as file:
                    logging.info(f"Processing file: {file_name}")
                    raw_data = json.load(file)
                    graph = parse_graph(raw_data)
                    viz_dag(graph, file_name.split(".")[0])
            except Exception as e:
                logging.error(f"Error processing file {file_name}: {e}")


if __name__ == "__main__":
    viz_graphs()
