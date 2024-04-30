import json
import pytest
from pathlib import Path

from app.io import parse_graph, CycleDetectedError, OrphanNodeError, NoRootError, MoreThanOneRootError
from app.workflow_runnner import run_node


# Fixtures loading test data
@pytest.fixture
def test_1_graph():
    data_path = Path(__file__).parent / "data" / "workflow_1.json"
    with open(data_path, "r") as file:
        return parse_graph(json.load(file))


@pytest.fixture
def test_2_graph():
    data_path = Path(__file__).parent / "data" / "workflow_2.json"
    with open(data_path, "r") as file:
        return parse_graph(json.load(file))


def test_simple_dag(test_1_graph):
    # Access test data
    assert len(test_1_graph.nodes) == 3
    assert test_1_graph.root.id == "A"


def test_process_node(test_1_graph):
    # Do all the nodes get processed?
    run_node(test_1_graph.root)
    for node in test_1_graph.nodes.values():
        assert node.run_count == 1

def test_complex_dag(test_2_graph):
    # test dag having multiple paths thru the same node
    run_node(test_2_graph.root)
    assert test_2_graph.get_node("E").run_count == 2

def test_orphan_node():
    # test that an orphan node raises an exception
    with pytest.raises(OrphanNodeError):
        data_path = Path(__file__).parent / "data" / "error_conditions" / "orphan_node.json"
        with open(data_path, "r") as file:
            parse_graph(json.load(file))

def test_no_root():
    # test that a graph with no root raises an exception
    with pytest.raises(NoRootError):
        data_path = Path(__file__).parent / "data" / "error_conditions" / "no_root.json"
        with open(data_path, "r") as file:
            parse_graph(json.load(file))

def test_more_than_one_root():
    # test that a graph with more than one root raises an exception
    with pytest.raises(MoreThanOneRootError):
        data_path = Path(__file__).parent / "data" / "error_conditions" / "2_root.json"
        with open(data_path, "r") as file:
            parse_graph(json.load(file))

def test_cycle_detected():
    # test that a graph with a cycle raises an exception
    with pytest.raises(CycleDetectedError):
        data_path = Path(__file__).parent / "data" / "error_conditions" / "looped.json"
        with open(data_path, "r") as file:
            parse_graph(json.load(file))