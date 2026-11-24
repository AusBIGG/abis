#!/usr/bin/env python3
"""Record, verify and compare the authoritative TDWG Darwin Core metadata."""

import argparse
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "schemas/background/dwc-metadata"
DWC = "http://rs.tdwg.org/dwc/terms/"
DCT = Namespace("http://purl.org/dc/terms/")
FILES = {
    "terms": ("https://rs.tdwg.org/dump/terms.ttl", ROOT / "schemas/background/dwc.ttl"),
    "term_list": ("https://rs.tdwg.org/dwc/terms.ttl", META / "term-list.ttl"),
    "vocabulary": ("https://rs.tdwg.org/dwc.ttl", META / "vocabulary.ttl"),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def graph(data):
    return Graph().parse(data=data, format="turtle")


def release(g, subject):
    dates = list(g.objects(URIRef(subject), DCT.modified))
    if len(dates) > 1:
        raise ValueError(f"Ambiguous modification date for {subject}: {dates}")
    versions = sorted(str(v) for v in g.objects(URIRef(subject), DCT.hasVersion))
    if not versions:
        raise ValueError(f"Missing version history for {subject}")
    version_dates = {v: date.fromisoformat(v.rsplit("/", 1)[-1]).isoformat() for v in versions}
    latest = max(version_dates.values())
    matching = [v for v in versions if version_dates[v] == latest]
    if len(matching) != 1:
        raise ValueError(f"No unique latest version IRI for {subject}")
    if dates and str(dates[0]) != latest:
        raise ValueError(f"Modification date and latest version disagree for {subject}")
    return {"iri": subject, "modified": str(dates[0]) if dates else None,
            "latest_version_date": latest, "version_iri": matching[0]}


def validate_bundle(data):
    graphs = {key: graph(value) for key, value in data.items()}
    terms = graphs["terms"]
    listed = set(graphs["term_list"].objects(URIRef(DWC), DCT.hasPart))
    defined = {s for s in terms.subjects(RDFS.isDefinedBy, URIRef(DWC))}
    if not listed or not listed <= defined:
        raise ValueError("Term-list membership is empty or its terms are absent from the dump")
    for name, kind in [("scientificName", RDF.Property), ("Occurrence", RDFS.Class)]:
        if (URIRef(DWC + name), RDF.type, kind) not in terms:
            raise ValueError(f"Missing expected {name} declaration in TDWG dump")
    return {
        "term_list": release(graphs["term_list"], DWC),
        "vocabulary": release(graphs["vocabulary"], "http://rs.tdwg.org/dwc/"),
    }


def fetch_bundle():
    data, artifacts = {}, {}
    for key, (url, _) in FILES.items():
        request = Request(url, headers={"Accept": "text/turtle", "User-Agent": "ABIS-DwC-metadata/1"})
        with urlopen(request, timeout=60) as response:
            data[key] = response.read()
            artifacts[key] = {
                "source_url": url,
                "resolved_url": response.url,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "sha256": digest(data[key]),
                "bytes": len(data[key]),
            }
    releases = validate_bundle(data)
    # Re-read the release records after fetching the dump to detect a release
    # moving during retrieval; do not accept a mixture of publication states.
    for key in ("term_list", "vocabulary"):
        with urlopen(Request(FILES[key][0], headers={"Accept": "text/turtle"}), timeout=60) as response:
            if response.read() != data[key]:
                raise ValueError("TDWG metadata changed during retrieval; retry the snapshot")
    return data, {"schema_version": 1, "releases": releases, "artifacts": artifacts}


def term_statements(g):
    result = {}
    for s, p, o in g:
        if isinstance(s, URIRef) and str(s).startswith(DWC):
            name = str(s)[len(DWC):]
            if name and "/" not in name and not name.endswith((".ttl", ".rdf", ".json", ".htm")):
                if not isinstance(o, (URIRef, Literal)):
                    raise ValueError("Blank-node term metadata needs a graph-isomorphic comparison")
                result.setdefault(str(s), set()).add((p.n3(), o.n3()))
    return result


def compare(before, after, term=None):
    def statements(data):
        g = graph(data)
        if term:
            canonical = URIRef(term)
            subjects = set(g.subjects(DCT.isVersionOf, canonical))
            if not subjects:
                subjects = {canonical} if any(g.triples((canonical, None, None))) else set()
            if len(subjects) != 1:
                raise ValueError(f"Expected one description/version for {term}, found {subjects}")
            subject = subjects.pop()
            return {term: {(p.n3(), o.n3()) for p, o in g.predicate_objects(subject)}}
        return term_statements(g)
    old, new = statements(before), statements(after)
    rows = []
    for term in sorted(old.keys() | new.keys()):
        removed = sorted(old.get(term, set()) - new.get(term, set()))
        added = sorted(new.get(term, set()) - old.get(term, set()))
        if removed or added:
            rows.append({"term": term, "status": "added" if term not in old else "removed" if term not in new else "changed",
                         "removed": removed, "added": added})
    return {"before_terms": len(old), "after_terms": len(new),
            "counts": {status: sum(r["status"] == status for r in rows) for status in ("added", "removed", "changed")},
            "changes": rows}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_local():
    snapshot = json.loads((META / "snapshot.json").read_text())
    if snapshot["schema_version"] != 1:
        raise ValueError("Unsupported snapshot schema version")
    data = {key: path.read_bytes() for key, (_, path) in FILES.items()}
    for key, value in data.items():
        expected = snapshot["artifacts"][key]
        if expected["source_url"] != FILES[key][0] or digest(value) != expected["sha256"] or len(value) != expected["bytes"]:
            raise ValueError(f"Snapshot provenance/checksum mismatch: {FILES[key][1]}")
    if validate_bundle(data) != snapshot["releases"]:
        raise ValueError("Snapshot release metadata mismatch")
    return data, snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Verify the recorded snapshot; optionally compare upstream")
    check.add_argument("--online", action="store_true")
    check.add_argument("--report", type=Path)
    refresh = sub.add_parser("refresh", help="Explicitly replace the snapshot after validating downloads")
    refresh.add_argument("--report", type=Path, required=True, help="Save the before/after term-level diff")
    diff = sub.add_parser("compare", help="Compare two local Turtle files without network access")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    diff.add_argument("--report", type=Path, required=True)
    diff.add_argument("--term", help="Compare one term's version documents using its canonical IRI")
    args = parser.parse_args()
    if args.command == "compare":
        report = compare(args.before.read_bytes(), args.after.read_bytes(), args.term)
        write_json(args.report, report)
        print(json.dumps(report["counts"]))
        return 0
    if args.command == "check":
        local, snapshot = check_local()
        print("Local snapshot verified:", snapshot["releases"]["term_list"]["version_iri"])
        if not args.online:
            return 0
        remote, candidate = fetch_bundle()
        changed = [key for key in FILES if local[key] != remote[key]]
        report = {"recorded_releases": snapshot["releases"], "upstream_releases": candidate["releases"],
                  "changed_artifacts": changed, "term_diff": compare(local["terms"], remote["terms"])}
        if args.report:
            write_json(args.report, report)
        print(json.dumps({"changed_artifacts": changed, "term_changes": report["term_diff"]["counts"]}))
        return 1 if changed else 0
    previous = FILES["terms"][1].read_bytes()
    data, snapshot = fetch_bundle()
    report = compare(previous, data["terms"])
    report.update({"before_sha256": digest(previous), "after_sha256": digest(data["terms"]), "upstream": snapshot})
    # All downloads, RDF parsing and consistency checks succeed before any writes.
    write_json(args.report, report)
    for key, (_, path) in FILES.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data[key])
    write_json(META / "snapshot.json", snapshot)
    check_local()
    print("Snapshot refreshed:", snapshot["releases"]["term_list"]["version_iri"])
    print(json.dumps(report["counts"]))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"DwC metadata check failed: {exc}", file=sys.stderr)
        sys.exit(2)
