# Changelog

All notable changes to **pii-radar** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/).

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
