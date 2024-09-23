from pathlib import Path
import pytest
from rdflib import Graph
from pyshacl import validate

TEST_DIR_PATH = Path(__file__).parent.resolve()


@pytest.fixture
def abis_shapes_graph():
    return Graph().parse(TEST_DIR_PATH.parent / "validators" / "abis-validator.ttl")


def test_abis_validator_01(abis_shapes_graph):
    g_sh = abis_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "monitor" / "cover-lite-valid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert conforms


def test_abis_validator_02(abis_shapes_graph):
    g_sh = abis_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "monitor" / "cover-lite-invalid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert not conforms


