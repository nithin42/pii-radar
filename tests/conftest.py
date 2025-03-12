"""
Shared pytest fixtures.
"""

from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path

import pytest


@pytest.fixture()
def tmp_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    """CSV file containing PII data for testing."""
    path = tmp_path / "sample.csv"
    rows = [
        ["name", "email", "phone", "notes"],
        ["Alice Smith", "alice@example.com", "555-123-4567", "Regular customer"],
        ["Bob Jones", "bob.jones@test.org", "+1 (800) 555-9999", "VIP member"],
        ["Charlie", "no-pii-here", "not a phone", "Safe record"],
        ["Dave", "dave@corp.io", "123-45-6789", "SSN in notes"],
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(rows)
    return path


@pytest.fixture()
def sample_json(tmp_path: Path) -> Path:
    """JSON file containing PII data for testing."""
    path = tmp_path / "sample.json"
    data = [
        {"id": 1, "user": "alice@example.com", "ip": "192.168.1.1"},
        {"id": 2, "user": "no-email", "ip": "not-an-ip"},
    ]
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.fixture()
def clean_csv(tmp_path: Path) -> Path:
    """CSV file with no PII."""
    path = tmp_path / "clean.csv"
    rows = [["product", "price", "category"], ["Widget", "9.99", "Tools"]]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(rows)
    return path
