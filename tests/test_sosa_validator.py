from pathlib import Path
import pytest
from rdflib import Graph
from pyshacl import validate

TEST_DIR_PATH = Path(__file__).parent.resolve()


@pytest.fixture
def sosa_shapes_graph():
    return Graph().parse(TEST_DIR_PATH.parent / "validators" / "sosa-validator.ttl")


def test_sosa_validator_01(sosa_shapes_graph):
    g_sh = sosa_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "sosa-valid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert conforms


def test_sosa_validator_02(sosa_shapes_graph):
    g_sh = sosa_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "sosa-invalid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert not conforms


