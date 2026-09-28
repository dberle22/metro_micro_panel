# Patterns in Place: Metro & Micro Panel

Patterns in Place: Metro & Micro Panel is a county-first public panel for all current US
metropolitan and micropolitan statistical areas: a static county-to-CBSA crosswalk plus annual
economics and affordability measures for 2012–2024.

## Release status

The repository is the public documentation and code home for the first release. `v2026.1` is an
immutable Zenodo dataset record with ZSTD Parquet files, a bundled DuckDB database,
`manifest.json`, and `coverage_report.md`.

[Download v2026.1 from Zenodo](https://zenodo.org/records/23020706) ·
[Version DOI](https://doi.org/10.5281/zenodo.23020706) ·
[Concept DOI](https://doi.org/10.5281/zenodo.23020705)

## Tables

| Table | Grain | Coverage |
| --- | --- | --- |
| `cbsa_county_crosswalk` | County-to-current-CBSA membership | OMB 2023; 1,915 memberships; 935 CBSAs |
| `economics_industry_wide` | CBSA-year | 2012–2024; ACS employment mix and optional county-derived BEA GDP measures |
| `affordability_wide` | CBSA-year | 2012–2024; ACS housing/income and optional county-derived HUD FMR measures |

## Using a published release

Download the versioned Zenodo release assets to one directory, then verify them before analysis:

```sh
python3 scripts/verify_release.py --release-dir path/to/v2026.1
```

Open the bundled DuckDB file with DuckDB, or query the Parquet files directly. Examples in
[`examples/`](examples/) show the analysis pattern; replace the input directory with the
published release directory or an HTTP location supplied by a future distribution mirror.

## Important caveats

- The crosswalk is static at the 2023 delineation vintage; it does not represent historical
  county membership.
- ACS values are five-year estimates. Adjacent years overlap and should not be read as
  independent annual samples.
- BEA GDP sector shares have uneven coverage. In particular, professional GDP share is available
  for 334–471 CBSAs per year, and education/health GDP share for 671–801. Check field coverage
  before analysis.
- HUD FMR source periods are fiscal years. All optional-field null counts appear in the versioned
  `coverage_report.md`.

## Documentation and citation

Read [Methodology](METHODOLOGY.md), the [table references](docs/),
[release history](RELEASES.md), [release-build approach](RELEASE_BUILD.md), and
[future-release notes](FUTURE_RELEASE_NOTES.md).

Release artifacts and documentation are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); code is MIT licensed. Cite:

> Berle, Dan. *Patterns in Place: Metro & Micro Panel*, v2026.1. Patterns in Place.
> https://doi.org/10.5281/zenodo.23020706

For the dataset as a whole across versions, cite the concept DOI
https://doi.org/10.5281/zenodo.23020705.
