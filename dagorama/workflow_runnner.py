import logging
import json
import os
import threading
import time

from dagorama import INPUT_DIR, OUTPUT_DIR
from dagorama.io import parse_graph, viz_dag
from dagorama.model import Node, Edge


def _process(edge: Edge) -> None:
    # this function simulates processing a node with a delay equal to the edge weight
    time.sleep(edge.weight)  
    run_node(edge.destination)  

def run_node(node: Node) -> None:
    # Recursively process a given node and all its children
    logging.info(f"Starting node: {node.id}")
    node.increment_run_count()
    threads = []
    for edge in node.edges_out:
        # Create a thread for each edge to handle the delay and subsequent node processing
        thread = threading.Thread(target=_process, args=(edge,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

def run_workflows() -> None:
    logging.info("Starting to process files")
    logging.info(f"Input: {INPUT_DIR}")
    logging.info(f"Output: {OUTPUT_DIR}")
    for file_name in os.listdir(INPUT_DIR):
        file_path = os.path.join(INPUT_DIR, file_name)
        if file_path.endswith('.json'):
            print(f"Processing file: {file_name}")
            with open(file_path, 'r') as file:
                raw_data = json.load(file)
                graph = parse_graph(raw_data)
                run_node(graph.root)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_workflows()
