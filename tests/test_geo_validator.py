from pathlib import Path
import pytest
from rdflib import Graph
from pyshacl import validate

TEST_DIR_PATH = Path(__file__).parent.resolve()

@pytest.fixture
def geo_shapes_graph():
    return Graph().parse(TEST_DIR_PATH.parent / "validators" / "geo-validator.ttl")


def test_geo_validator_01(geo_shapes_graph):
    g_sh = geo_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "geo-valid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert conforms


def test_geo_validator_02(geo_shapes_graph):
    g_sh = geo_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "geo-invalid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert not conforms
