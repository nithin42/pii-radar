"""
Core scanning engine — orchestrates readers and detectors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from pii_radar.detectors import PIIMatch, detect
from pii_radar.readers import read_file


@dataclass
class ScanResult:
    """Aggregated result for a single file scan."""

    file_path: Path
    total_cells_scanned: int = 0
    matches: List[PIIMatch] = field(default_factory=list)

    @property
    def total_matches(self) -> int:
        return len(self.matches)

    @property
    def pii_types_found(self) -> List[str]:
        return sorted({m.pii_type for m in self.matches})

    @property
    def columns_affected(self) -> List[str]:
        return sorted({m.column for m in self.matches})

    @property
    def is_clean(self) -> bool:
        return len(self.matches) == 0


def scan_file(
    path: Path,
    min_confidence: float = 0.0,
    sample_rows: Optional[int] = None,
) -> ScanResult:
    """
    Scan a single file for PII.

    Args:
        path: Path to the file to scan.
        min_confidence: Minimum confidence threshold (0.0–1.0).
                        Detections below this are filtered out.
        sample_rows: Optional row limit to scan (for quick audit sampling).

    Returns:
        ScanResult with all matches found.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file type is unsupported.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    result = ScanResult(file_path=path)

    for column, value, row_index in read_file(path):
        if sample_rows is not None and row_index >= sample_rows:
            continue
        result.total_cells_scanned += 1
        for match in detect(value, column, row_index):
            if match.confidence >= min_confidence:
                result.matches.append(match)

    return result


def scan_directory(
    directory: Path,
    min_confidence: float = 0.0,
    sample_rows: Optional[int] = None,
    extensions: tuple[str, ...] = (".csv", ".json", ".parquet", ".pq"),
) -> List[ScanResult]:
    """
    Recursively scan all supported files in a directory.

    Args:
        directory: Path to the directory.
        min_confidence: Minimum confidence threshold.
        sample_rows: Optional row limit to scan per file.
        extensions: File extensions to include.

    Returns:
        List of ScanResult, one per file found.
    """
    results: List[ScanResult] = []
    for ext in extensions:
        for filepath in directory.rglob(f"*{ext}"):
            results.append(
                scan_file(filepath, min_confidence=min_confidence, sample_rows=sample_rows)
            )
    return results
