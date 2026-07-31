# Changelog

All notable changes to **pii-radar** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

## [0.4.1] — 2026-07-31

### Added
- **IPv6 Regex Detection**: Added 128-bit IPv6 address pattern matching (`_IPV6_PATTERN`)
- **Optional Parquet Extra**: Made `pyarrow` optional (`pip install pii-radar[parquet]`) for lighter base installs
- **Test Coverage Validation**: Validated `test_negative_cases.py` and IPv6 detection in unit test suite

## [0.4.0] — 2026-07-31

### Added
- **Luhn Mod-10 Algorithm Checksum**: Validates credit card numbers to eliminate 16-digit account/order false positives
- **IPv4 Octet Range Validation**: Verifies 0-255 octet bounds and rejects version strings
- **DOB Column Heuristics**: Contextual matching on column headers (`dob`, `birth`, `birthday`, `bday`)
- **`--sample N` / `-s N` Flag**: Limits row scanning for rapid audit sampling on massive files
- **`tests/test_negative_cases.py`**: Comprehensive false-positive unit test suite
- **`examples/benchmark.py`**: Performance benchmarking script
- **Windows Runner**: Added `windows-latest` to GitHub Actions CI matrix

## [0.3.1] — 2026-07-30

### Added
- PyPI release via OIDC Pending Publisher

## [0.3.0] — 2026-07-30

### Added
- PyPI Trusted Publisher integration via OpenID Connect (OIDC)
- Dynamic Console instantiation for headless CliRunner output compatibility
- Pytest pythonpath options in pyproject.toml

## [0.2.0] — 2026-07-20

### Added
- Parquet file support (`.parquet`, `.pq`) via PyArrow
- `--fail-on-detect` flag for CI/CD pipeline integration
- Confidence scoring displayed per detection in terminal table
- Folder scanning with recursive file discovery (`scan directory/`)
- JSON output mode (`--output json`) for programmatic consumption

### Fixed
- False positive reduction in phone number detection for zip codes
- Encoding errors on Windows for UTF-16 encoded CSV files

### Changed
- Rich terminal output redesigned with panel summary + detailed table
- Improved SSN regex to reject invalid ranges (000-xx, 666-xx)

---

## [0.1.0] — 2025-06-25

### Added
- Initial release of `pii-radar`
- CLI command: `pii-radar scan <file>`
- PII detectors: EMAIL, PHONE, SSN, CREDIT_CARD, IP_ADDRESS, DATE_OF_BIRTH
- CSV and JSON file reader support
- `--output table/json` flag
- `--min-confidence` threshold filtering
- `--report` flag to save matches to CSV
- `--redact` flag to create a sanitized CSV copy
- GitHub Actions CI across Python 3.9–3.12
- Pre-commit hooks: black, flake8, bandit

<!-- Updated Jun 2026 -->

<!-- v0.2.0 finalized -->
