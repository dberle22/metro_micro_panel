#!/usr/bin/env python3
"""Verify a downloaded Metro & Micro Panel release without private Foundations access."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import duckdb


def sha256(path: Path) -> str:
    """Return the artifact hash used by the release manifest."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def columns(connection: duckdb.DuckDBPyConnection, relation: str) -> list[str]:
    """Read ordered column names from a named table."""

    return [row[0] for row in connection.execute(f"DESCRIBE {relation}").fetchall()]


def verify_release(release_dir: Path) -> None:
    """Check hashes, row counts, and schemas declared in a public manifest.

    The verifier deliberately consumes only downloaded public artifacts. It establishes that the
    files are the documented release, without pretending to rebuild the private source pipeline.
    """

    manifest_path = release_dir / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"Missing manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text())

    bundled = release_dir / manifest["bundled_duckdb"]["file"]
    if not bundled.is_file():
        raise ValueError(f"Missing bundled DuckDB: {bundled}")
    if sha256(bundled) != manifest["bundled_duckdb"]["sha256"]:
        raise ValueError("Bundled DuckDB hash does not match manifest.")

    with duckdb.connect(str(bundled), read_only=True) as bundled_connection:
        for table_name, table_manifest in manifest["tables"].items():
            parquet = release_dir / table_manifest["parquet"]["file"]
            if not parquet.is_file():
                raise ValueError(f"Missing Parquet for {table_name}: {parquet}")
            if sha256(parquet) != table_manifest["parquet"]["sha256"]:
                raise ValueError(f"Parquet hash does not match manifest for {table_name}.")

            expected_columns = [column["name"] for column in table_manifest["columns"]]
            bundled_columns = columns(bundled_connection, f'"{table_name}"')
            # `DESCRIBE SELECT` accepts a bound path and avoids treating a table function as
            # a table identifier. It also keeps paths with spaces or quotes safe.
            parquet_columns = [
                row[0]
                for row in bundled_connection.execute(
                    "DESCRIBE SELECT * FROM read_parquet(?)", [str(parquet)]
                ).fetchall()
            ]
            if bundled_columns != expected_columns or parquet_columns != expected_columns:
                raise ValueError(f"Schema does not match manifest for {table_name}.")

            bundled_rows = bundled_connection.execute(
                f'SELECT count(*) FROM "{table_name}"'
            ).fetchone()[0]
            parquet_rows = bundled_connection.execute(
                "SELECT count(*) FROM read_parquet(?)", [str(parquet)]
            ).fetchone()[0]
            if bundled_rows != table_manifest["row_count"] or parquet_rows != bundled_rows:
                raise ValueError(f"Row count does not match manifest for {table_name}.")

    print(f"Verified {manifest['title']} {manifest['version']} in {release_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-dir", required=True, type=Path)
    verify_release(parser.parse_args().release_dir)


if __name__ == "__main__":
    main()
