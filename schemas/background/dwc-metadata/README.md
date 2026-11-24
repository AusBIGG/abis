# Darwin Core metadata snapshot

`../dwc.ttl` is the unmodified response from TDWG's [core-term dump](https://rs.tdwg.org/dump/terms.ttl). It includes deprecated terms and per-term histories. It is reference metadata, not an additional ABIS validation policy or an OWL graph model. Refreshing it does not change ABIS mappings, shapes, or instance data.

`term-list.ttl` records membership and release links for the core namespace. `vocabulary.ttl` records the broader Darwin Core vocabulary and its constituent term lists. `snapshot.json` records source and resolved URLs, UTC retrieval times, exact byte counts and SHA-256 checksums, plus both release IRIs. Git preserves accepted snapshots over time; do not overwrite old commits to refresh them.

The current term-list RDF does not supply `dcterms:modified` on the term-list resource. The checker records that value as `null` and derives `latest_version_date` from its explicit, date-form version IRIs. It does not pretend that the inferred release date is a supplied modification date. The HTML issue date and the whole-vocabulary RDF modification date are separate evidence.

## Verify the accepted snapshot

From the repository root, in a Python 3.12+ virtual environment:

```sh
python -m pip install -r scripts/requirements-dwc.txt
python scripts/dwc_metadata.py check
python -m unittest discover -s tests -p test_dwc_metadata.py -v
```

The offline check verifies all three response checksums, parses their RDF, checks release metadata, and verifies that the term list's members are present in the dump. It detects accidental edits to the reference files without requiring a public service.

## Check for upstream changes

```sh
python scripts/dwc_metadata.py check --online --report dwc-upstream-comparison.json
```

Exit status `0` means the downloaded artifacts match; `1` means upstream differs; `2` indicates a download, parse, or integrity error. This command does not change the accepted snapshot. It compares response bytes as well as term-level RDF statements, so a changed definition is reported even when TDWG did not change a date. Serialization-only changes still flag a changed artifact but produce no term-statement changes. The report separates byte drift from term changes and reports release metadata separately.

The GitHub workflow verifies the accepted snapshot on relevant pull requests and pushes. A weekly Monday 00:00 UTC check, or manual workflow run, also checks upstream and saves the comparison as a workflow artifact. A difference fails the check for maintainer review; the workflow does not commit or publish updates. Scheduled checks start once this workflow is on the default branch.

## Accept a new snapshot

```sh
python scripts/dwc_metadata.py refresh --report dwc-refresh-changes.json
python scripts/dwc_metadata.py check
```

Run refresh in a change branch. Review the report and RDF diff, particularly changed definitions, deprecations, replacements, class/property types and namespace use. The tool validates all downloads and rechecks the release records before writing; any download/validation failure leaves the accepted files intact. Commit the three response files and `snapshot.json` together. Keep the comparison report with the review evidence. There is no live-SPARQL dependency.

On systems whose Python environment lacks the operating system CA trust configuration, configure a trusted CA bundle, for example `SSL_CERT_FILE=/etc/ssl/cert.pem` on the workspace Mac. Do not disable certificate verification.

## Explain a specific term change

Download the two published version documents, then compare them using the canonical term IRI. This aligns the version-specific subjects before comparing their predicates and values:

```sh
python scripts/dwc_metadata.py compare associatedReferences-2023-06-28.ttl associatedReferences-2026-10-13.ttl --term http://rs.tdwg.org/dwc/terms/associatedReferences --report associatedReferences-changes.json
```

The same `compare` command without `--term` compares all canonical core-term descriptions in two dumps. Neither mode relies on history notes. Dates, version/status links and editorial metadata appear alongside substantive changes, so the reviewer can distinguish them.

## Scope

This snapshots the core `dwc:` namespace only. The broader vocabulary also references `dwciri:`, borrowed terms and extensions; those require their own term-list artifacts if added to this mechanism. Imported TERN ontologies and BDR-specific SHACL rules remain independently versioned. A TDWG metadata update does not automatically establish that those models or shapes should be upgraded.
