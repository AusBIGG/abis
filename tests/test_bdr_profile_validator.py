from pathlib import Path
import pytest
from rdflib import Graph
from pyshacl import validate

TEST_DIR_PATH = Path(__file__).parent.resolve()


@pytest.fixture
def bdr_profile_shapes_graph():
    return Graph().parse(TEST_DIR_PATH.parent / "validators" / "bdr-profile-validator.ttl")


def test_bdr_protocol_validator_01(bdr_profile_shapes_graph):
    g_sh = bdr_profile_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "bdr-01-valid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    if not conforms:
        print(results_text)
    assert conforms


def test_bdr_protocol_validator_02(bdr_profile_shapes_graph):
    g_sh = bdr_profile_shapes_graph
    g_data = Graph().parse(TEST_DIR_PATH / "data" / "bdr-02-invalid.ttl")

    conforms, results_graph, results_text = validate(g_data, shacl_graph=g_sh)
    assert not conforms


