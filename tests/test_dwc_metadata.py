"""Regression tests for snapshot integrity and changes not represented by dates."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from rdflib import Graph

SPEC = importlib.util.spec_from_file_location("dwc_metadata", Path(__file__).parents[1] / "scripts/dwc_metadata.py")
metadata = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(metadata)


class SnapshotTests(unittest.TestCase):
    def test_committed_snapshot_is_complete_and_verified(self):
        data, snapshot = metadata.check_local()
        self.assertGreater(len(metadata.graph(data["terms"])), 1000)
        self.assertIn("version_iri", snapshot["releases"]["term_list"])

    def test_term_list_without_modified_uses_explicit_version_links(self):
        g = Graph().parse(data='''
            @prefix d: <http://purl.org/dc/terms/> .
            <https://example.org/list> d:hasVersion <https://example.org/version/2026-01-01>,
                <https://example.org/version/2026-10-13> .
        ''', format="turtle")
        release = metadata.release(g, "https://example.org/list")
        self.assertIsNone(release["modified"])
        self.assertEqual(release["latest_version_date"], "2026-10-13")

    def test_changed_definition_is_detected_without_a_date_change(self):
        before = b'@prefix dwc: <http://rs.tdwg.org/dwc/terms/> . dwc:scientificName <https://example.org/definition> "old"@en .'
        after = before.replace(b'"old"', b'"new"')
        result = metadata.compare(before, after)
        self.assertEqual(result["counts"]["changed"], 1)
        self.assertIn('"old"@en', result["changes"][0]["removed"][0])

    def test_prefix_and_statement_order_do_not_count_as_term_changes(self):
        before = b'@prefix dwc: <http://rs.tdwg.org/dwc/terms/> . dwc:scientificName <https://example.org/p> "name" .'
        after = b'<http://rs.tdwg.org/dwc/terms/scientificName> <https://example.org/p> "name" .'
        self.assertEqual(metadata.compare(before, after)["changes"], [])

    def test_version_documents_are_compared_as_the_same_term(self):
        before = b'''@prefix d: <http://purl.org/dc/terms/> .
            <https://example.org/v1> d:isVersionOf <https://example.org/term> ;
                <https://example.org/definition> "old" .'''
        after = before.replace(b"/v1>", b"/v2>").replace(b'"old"', b'"new"')
        result = metadata.compare(before, after, "https://example.org/term")
        self.assertEqual(result["counts"], {"added": 0, "removed": 0, "changed": 1})

    def test_checksum_detects_tampering_even_if_rdf_is_still_valid(self):
        _, snapshot = metadata.check_local()
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "dwc.ttl"
            target.write_bytes(metadata.FILES["terms"][1].read_bytes() + b'\n# unexpected edit\n')
            files = dict(metadata.FILES)
            files["terms"] = (files["terms"][0], target)
            with patch.object(metadata, "FILES", files):
                with self.assertRaisesRegex(ValueError, "checksum mismatch"):
                    metadata.check_local()

    def test_download_failure_leaves_snapshot_unchanged(self):
        before = {key: path.read_bytes() for key, (_, path) in metadata.FILES.items()}
        with patch.object(metadata, "fetch_bundle", side_effect=ValueError("invalid upstream RDF")):
            with patch("sys.argv", ["dwc_metadata.py", "refresh", "--report", "/unused/report.json"]):
                with self.assertRaisesRegex(ValueError, "invalid upstream RDF"):
                    metadata.main()
        self.assertEqual(before, {key: path.read_bytes() for key, (_, path) in metadata.FILES.items()})

    def test_online_drift_fails_without_replacing_snapshot(self):
        data, snapshot = metadata.check_local()
        candidate = dict(data)
        candidate["terms"] += b'\n# upstream serialization change\n'
        with patch.object(metadata, "fetch_bundle", return_value=(candidate, snapshot)):
            with patch("sys.argv", ["dwc_metadata.py", "check", "--online"]):
                self.assertEqual(metadata.main(), 1)
        self.assertEqual(metadata.FILES["terms"][1].read_bytes(), data["terms"])


if __name__ == "__main__":
    unittest.main()
