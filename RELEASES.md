# Releases

## v2026.1

**Status:** pre-publication release candidate.

This first version contains:

- OMB 2023 static county-to-CBSA crosswalk for all 935 current CBSAs.
- 2012–2024 ACS employment-composition and affordability measures.
- 2012–2024 county-derived BEA real GDP total and three optional industry shares.
- FY2012–FY2024 county-derived HUD two-bedroom FMR and FMR gap.

The eventual immutable release directory will contain three ZSTD Parquet files, one bundled
DuckDB file, `manifest.json`, and a generated `coverage_report.md`. The manifest records
artifact hashes and release-specific provenance. The final publication entry will add the
canonical data URL, version DOI, concept DOI, and publication date after they exist.
