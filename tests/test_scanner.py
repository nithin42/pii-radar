"""Unit tests for pii_radar.scanner module."""

from __future__ import annotations

import pytest
from pathlib import Path
from pii_radar.scanner import scan_file, scan_directory, ScanResult


class TestScanFile:
    def test_scan_csv_detects_email(self, sample_csv: Path):
        result = scan_file(sample_csv)
        assert isinstance(result, ScanResult)
        assert result.total_matches > 0
        assert "EMAIL" in result.pii_types_found

    def test_scan_json_detects_email_and_ip(self, sample_json: Path):
        result = scan_file(sample_json)
        assert "EMAIL" in result.pii_types_found
        assert "IP_ADDRESS" in result.pii_types_found

    def test_scan_clean_file_is_clean(self, clean_csv: Path):
        result = scan_file(clean_csv)
        assert result.is_clean
        assert result.total_matches == 0

    def test_scan_nonexistent_file_raises(self, tmp_path: Path):
        with pytest.raises(FileNotFoundError):
            scan_file(tmp_path / "ghost.csv")

    def test_scan_unsupported_extension_raises(self, tmp_path: Path):
        bad_file = tmp_path / "data.xlsx"
        bad_file.write_text("data")
        with pytest.raises(ValueError, match="Unsupported file type"):
            scan_file(bad_file)

    def test_scan_result_has_file_path(self, sample_csv: Path):
        result = scan_file(sample_csv)
        assert result.file_path == sample_csv

    def test_min_confidence_filters_results(self, sample_csv: Path):
        result_low = scan_file(sample_csv, min_confidence=0.0)
        result_high = scan_file(sample_csv, min_confidence=0.99)
        assert result_high.total_matches <= result_low.total_matches

    def test_columns_affected_populated(self, sample_csv: Path):
        result = scan_file(sample_csv)
        assert len(result.columns_affected) > 0


class TestScanDirectory:
    def test_scans_multiple_files(self, tmp_path: Path, sample_csv: Path, sample_json: Path):
        import shutil
        sub = tmp_path / "subdir"
        sub.mkdir()
        shutil.copy(sample_csv, sub / "a.csv")
        shutil.copy(sample_json, sub / "b.json")
        results = scan_directory(sub)
        assert len(results) == 2

    def test_returns_empty_for_empty_directory(self, tmp_path: Path):
        sub = tmp_path / "empty_dir"
        sub.mkdir()
        results = scan_directory(sub)
        assert results == []

    def test_respects_extension_filter(self, tmp_path: Path, sample_csv: Path):
        import shutil
        sub = tmp_path / "filter_dir"
        sub.mkdir()
        shutil.copy(sample_csv, sub / "data.csv")
        results = scan_directory(sub, extensions=(".json",))
        assert results == []
