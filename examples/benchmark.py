"""
Reproducible performance benchmark script for pii-radar.

Generates synthetic CSV data and measures throughput (cells/second).

Usage:
    python examples/benchmark.py
"""

from __future__ import annotations

import csv
import tempfile
import time
from pathlib import Path

from pii_radar.scanner import scan_file


def generate_benchmark_csv(path: Path, num_rows: int = 10000) -> int:
    """Generate a synthetic CSV file for benchmark testing."""
    headers = ["user_id", "full_name", "email", "phone_number", "ssn", "ip_address", "created_at"]
    rows = []
    for i in range(num_rows):
        rows.append(
            [
                str(i),
                f"User_{i}",
                f"user_{i}@example.com" if i % 2 == 0 else "plain_username",
                f"555-{i:03d}-1234" if i % 3 == 0 else "N/A",
                f"{i%900+100:03d}-45-{i%9000+1000:04d}" if i % 5 == 0 else "000-00-0000",
                f"192.168.1.{(i % 250) + 1}" if i % 4 == 0 else "not-an-ip",
                "2024-05-10",
            ]
        )

    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)

    return num_rows * len(headers)


def main() -> None:
    print("🚀 Running pii-radar Performance Benchmark...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        csv_path = Path(tmp_dir) / "benchmark_10k.csv"
        num_rows = 10000
        print(f"Generating benchmark CSV ({num_rows:,} rows)...")
        total_cells = generate_benchmark_csv(csv_path, num_rows=num_rows)
        file_size_mb = csv_path.stat().st_size / (1024 * 1024)
        print(f"Dataset ready: {file_size_mb:.2f} MB, {total_cells:,} total cells.\n")

        start_time = time.perf_counter()
        result = scan_file(csv_path)
        elapsed_sec = time.perf_counter() - start_time

        cells_per_sec = result.total_cells_scanned / elapsed_sec if elapsed_sec > 0 else 0

        print("📊 Benchmark Results:")
        print(f"  • Total Execution Time: {elapsed_sec:.3f} seconds")
        print(f"  • Total Cells Scanned:  {result.total_cells_scanned:,}")
        print(f"  • PII Matches Found:    {result.total_matches:,}")
        print(f"  • PII Types Detected:   {', '.join(result.pii_types_found)}")
        print(f"  • Throughput:           {cells_per_sec:,.0f} cells/second\n")
        print("✅ Benchmark complete.")


if __name__ == "__main__":
    main()
