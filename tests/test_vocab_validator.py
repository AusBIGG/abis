from pathlib import Path
import pytest
from rdflib import Graph
from pyshacl import validate

TEST_DIR_PATH = Path(__file__).parent.resolve()


@pytest.fixture
def vocpub_shapes_graph():
    return Graph().parse(TEST_DIR_PATH.parent / "validators" / "vocpub-validator.ttl")


def test_sosa_validator_01(vocpub_shapes_graph):
    g_sh = vocpub_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "vocpub-valid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert conforms


def test_sosa_validator_02(vocpub_shapes_graph):
    g_sh = vocpub_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "vocpub-invalid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert not conforms

