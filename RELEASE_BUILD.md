# Release-build approach

## What this repository publishes

This repository contains the public release contract: documentation, examples, citation and
license metadata, change history, and a verifier for downloaded artifacts. It does not contain
the private Foundations warehouse, raw source extracts, or the private transformation pipeline.

## How a version is made

Each version is built internally from documented US federal source families using a static
county-to-CBSA crosswalk. Before publication, the release process enforces the approved table
and column boundary, validates keys and geographic coverage, and writes:

- one ZSTD-compressed Parquet file for each public table;
- one bundled DuckDB database with the same tables;
- `manifest.json`, with ordered schemas, row counts, field provenance, and SHA-256 hashes; and
- `coverage_report.md`, with annual geography and non-null coverage.

The published [Methodology](METHODOLOGY.md) and [table references](docs/) describe every
released field's source family, upstream variable, definition, units, coverage, and null
behavior. The [Changelog](CHANGELOG.md) records any public-contract change.

## Verifying a downloaded version

After downloading all artifacts from a versioned Zenodo record into one directory, run:

```sh
python3 scripts/verify_release.py --release-dir path/to/v2026.1
```

The verifier checks every Parquet and DuckDB SHA-256 hash, each table's ordered schema, and its
row count against `manifest.json`. It can establish that a download is the documented release;
it does not reproduce the private source pipeline.

## Versioning rule

Published releases are immutable. A correction or refresh is a new version with its own assets,
manifest, coverage report, changelog entry, and Zenodo DOI version record. No upstream revision
silently changes an existing release.
