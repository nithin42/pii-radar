"""
Output formatting and reporting for PII scan results.

Supports: rich terminal table, JSON, CSV.
"""

from __future__ import annotations

import json
import csv
import sys
from io import StringIO
from pathlib import Path
from typing import List

from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text

from pii_radar.scanner import ScanResult

console = Console()


def print_summary(results: List[ScanResult]) -> None:
    """Print a high-level summary panel to the terminal."""
    total_files = len(results)
    clean_files = sum(1 for r in results if r.is_clean)
    flagged_files = total_files - clean_files
    total_matches = sum(r.total_matches for r in results)
    total_cells = sum(r.total_cells_scanned for r in results)

    color = "green" if flagged_files == 0 else "red"
    status = "✅ ALL CLEAN" if flagged_files == 0 else f"⚠️  {flagged_files} FILE(S) WITH PII"

    summary = (
        f"[bold]Files Scanned:[/bold]  {total_files}\n"
        f"[bold]Cells Scanned:[/bold]  {total_cells:,}\n"
        f"[bold]PII Matches:[/bold]    {total_matches}\n"
        f"[bold]Status:[/bold]         [{color}]{status}[/{color}]"
    )
    console.print(Panel(summary, title="[bold cyan]pii-radar — Scan Summary[/bold cyan]", expand=False))


def print_table(results: List[ScanResult]) -> None:
    """Render a rich table of all PII matches to the terminal."""
    flagged = [r for r in results if not r.is_clean]

    if not flagged:
        console.print("[bold green]✅ No PII detected in any scanned files.[/bold green]")
        return

    for result in flagged:
        table = Table(
            title=f"📄 {result.file_path.name}",
            box=box.ROUNDED,
            show_lines=True,
            header_style="bold magenta",
        )
        table.add_column("Row", style="dim", width=6)
        table.add_column("Column", style="cyan")
        table.add_column("PII Type", style="bold red")
        table.add_column("Redacted Value", style="yellow")
        table.add_column("Confidence", justify="right")

        for match in result.matches:
            confidence_bar = _confidence_bar(match.confidence)
            table.add_row(
                str(match.row_index),
                match.column,
                match.pii_type,
                match.value,
                confidence_bar,
            )

        console.print(table)


def print_json(results: List[ScanResult]) -> None:
    """Print JSON-formatted results to stdout (for CI/CD integration)."""
    output = []
    for result in results:
        output.append(
            {
                "file": str(result.file_path),
                "total_cells": result.total_cells_scanned,
                "total_matches": result.total_matches,
                "pii_types": result.pii_types_found,
                "columns_affected": result.columns_affected,
                "matches": [
                    {
                        "row": m.row_index,
                        "column": m.column,
                        "type": m.pii_type,
                        "value": m.value,
                        "confidence": round(m.confidence, 2),
                    }
                    for m in result.matches
                ],
            }
        )
    console.print_json(json.dumps(output, indent=2))


def save_csv_report(results: List[ScanResult], output_path: Path) -> None:
    """Save all matches to a CSV report file."""
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["file", "row", "column", "pii_type", "value", "confidence"],
        )
        writer.writeheader()
        for result in results:
            for match in result.matches:
                writer.writerow(
                    {
                        "file": str(result.file_path),
                        "row": match.row_index,
                        "column": match.column,
                        "pii_type": match.pii_type,
                        "value": match.value,
                        "confidence": round(match.confidence, 2),
                    }
                )


def _confidence_bar(confidence: float) -> str:
    """Render a compact confidence percentage string with color."""
    pct = int(confidence * 100)
    if pct >= 90:
        return f"[green]{pct}%[/green]"
    if pct >= 75:
        return f"[yellow]{pct}%[/yellow]"
    return f"[red]{pct}%[/red]"

# Confidence displayed as color-coded percentage per detection
