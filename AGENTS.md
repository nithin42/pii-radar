# AGENTS.md — AI Context for pii-radar

## Project Identity
**pii-radar** is a production-grade Python CLI tool for detecting Personally Identifiable Information (PII) in structured data files (CSV, JSON, Parquet).

## Portfolio Context
Part of **Nithin's elite Data Science & Secure Computing portfolio** (Pillar 2 — Open Source Core Tools).
Aligns with research interests in data privacy, GDPR compliance, and secure ML pipelines.

## Architecture
```
src/pii_radar/
├── cli.py         ← Click CLI entry point (scan command + flags)
├── scanner.py     ← Orchestrates file reading + detection (ScanResult)
├── detectors.py   ← Regex-based PII pattern matching (PIIMatch)
├── readers.py     ← CSV / JSON / Parquet file parsers
└── reporter.py    ← Rich terminal tables, JSON output, CSV report
```

## Design Decisions
- **No ML/NLP dependency** — pure regex for speed and zero model download overhead
- **Rich** for terminal output — beautiful tables and panels
- **Click** for CLI — idiomatic, testable, well-documented
- **Modular** — detectors, readers, and reporters are independently testable
- **`--fail-on-detect`** flag makes it CI/CD friendly (pre-commit, GitHub Actions)

## Key Interfaces
- `scan_file(path, min_confidence)` → `ScanResult`
- `scan_directory(directory, min_confidence)` → `List[ScanResult]`
- `detect(value, column, row_index)` → `List[PIIMatch]`

## Coding Standards
- Python 3.9+ with full type hints (mypy strict)
- Black formatting, flake8 linting
- All public functions have docstrings
- Unit tests in `tests/` with pytest, target ≥ 85% coverage

## What NOT to Change
- Do not add ML/NLP models — keep the tool lightweight
- Do not break the `PIIMatch` dataclass interface (used by downstream tools)
- Do not change the `scan_file` return type
