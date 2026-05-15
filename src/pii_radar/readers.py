"""
File readers for CSV, JSON, and Parquet formats.

Returns a unified list of (column_name, value, row_index) tuples
ready for PII scanning.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Generator, Tuple

import pandas as pd


# Type alias for a single scannable cell
Cell = Tuple[str, str, int]  # (column, value, row_index)


def read_file(path: Path) -> Generator[Cell, None, None]:
    """
    Dispatch to the appropriate reader based on file extension.

    Args:
        path: Path to the file.

    Yields:
        (column, value, row_index) tuples for every cell in the file.

    Raises:
        ValueError: If the file extension is not supported.
    """
    suffix = path.suffix.lower()
    if suffix == ".csv":
        yield from _read_csv(path)
    elif suffix == ".json":
        yield from _read_json(path)
    elif suffix in (".parquet", ".pq"):
        yield from _read_parquet(path)
    else:
        raise ValueError(
            f"Unsupported file type: '{suffix}'. "
            "Supported: .csv, .json, .parquet, .pq"
        )


def _read_csv(path: Path) -> Generator[Cell, None, None]:
    """Read a CSV file and yield all non-null string cells."""
    try:
        df = pd.read_csv(path, dtype=str, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(path, dtype=str, encoding="latin-1", low_memory=False)

    yield from _iter_dataframe(df)


def _read_json(path: Path) -> Generator[Cell, None, None]:
    """Read a JSON file (array or object) and yield all string cells."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    if isinstance(data, list):
        df = pd.json_normalize(data)
    elif isinstance(data, dict):
        df = pd.json_normalize([data])
    else:
        raise ValueError("JSON must be an object or array of objects.")

    df = df.astype(str)
    yield from _iter_dataframe(df)


def _read_parquet(path: Path) -> Generator[Cell, None, None]:
    """Read a Parquet file and yield all string-convertible cells."""
    df = pd.read_parquet(path).astype(str)
    yield from _iter_dataframe(df)


def _iter_dataframe(df: pd.DataFrame) -> Generator[Cell, None, None]:
    """Iterate over every cell of a DataFrame and yield (col, value, row)."""
    for col in df.columns:
        for row_idx, value in enumerate(df[col]):
            if value and value not in ("nan", "None", ""):
                yield col, str(value), row_idx

# Supports UTF-8 and latin-1 fallback for legacy CSV files

# Parquet support via pyarrow - supports .parquet and .pq extensions
