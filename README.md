<div align="center">

# 🔍 pii-radar

**Scan any CSV, JSON, or Parquet file for Personally Identifiable Information — in seconds.**

[![CI](https://github.com/nithin42/pii-radar/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/nithin42/pii-radar/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-87%25-brightgreen)](https://github.com/nithin42/pii-radar)
[![PyPI version](https://badge.fury.io/py/pii-radar.svg?v=0.4.1)](https://pypi.org/project/pii-radar/)
[![Python](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://pypi.org/project/pii-radar/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

---

## Abstract

Data engineers and ML practitioners routinely work with datasets that silently contain Personally Identifiable Information (PII) — emails, phone numbers, SSNs, credit card numbers, and IP addresses — creating compliance risks under GDPR, CCPA, and HIPAA. **pii-radar** is a lightweight, zero-dependency-ML CLI tool that scans structured data files for PII using high-precision patterns, Luhn Mod-10 verification, and contextual heuristics, outputting results as rich terminal tables, JSON, or CSV reports. It integrates natively with pre-commit hooks and GitHub Actions to catch PII before it reaches production or version control.

---

## ✨ Features

- 🔎 **6 PII types detected** — Email, Phone, SSN, Credit Card (Luhn validated), IP Address (IPv4 & IPv6), Date of Birth (Heuristic)
- 📁 **3 file formats** — CSV, JSON, Parquet (`.parquet`, `.pq`)
- 📂 **Folder scanning** — Recursively scan entire directories
- 🎨 **Beautiful terminal output** — Rich tables with confidence scores
- 🤖 **CI/CD native** — `--fail-on-detect` exits with code 1 for pipeline gates
- ⚡ **Row sampling** — `--sample 1000` limit for rapid audit sampling on massive files
- 🔒 **Auto-redaction** — `--redact` creates a sanitized copy of your data
- 📊 **CSV reports** — Save all findings to a structured report file
- ⚡ **Fast** — Pure regex + algorithmic validation, no heavy ML models

---

## 📦 Installation

```bash
# Base installation (Lightweight)
pip install pii-radar

# With Parquet support
pip install "pii-radar[parquet]"
```

Or install from source:

```bash
git clone https://github.com/nithin42/pii-radar.git
cd pii-radar
pip install -e ".[dev]"
```

---

## 🚀 Quick Start

```bash
# Scan a CSV file
pii-radar scan data/customers.csv

# Fast sampling (scan only first 1,000 rows)
pii-radar scan data/large_file.csv --sample 1000

# Scan a JSON file
pii-radar scan logs/events.json

# Scan an entire directory
pii-radar scan data/

# Get JSON output (great for scripts)
pii-radar scan data.csv --output json

# Only show high-confidence detections
pii-radar scan data.csv --min-confidence 0.9

# Save a report to CSV
pii-radar scan data.csv --report pii_report.csv

# Create a redacted copy
pii-radar scan data.csv --redact data_clean.csv

# Use in CI/CD — fails build if PII found
pii-radar scan data.csv --fail-on-detect
```

---

## 🏗️ Architecture

```
CLI Interface (cli.py)
   │
   ├─► scan_file / scan_directory (scanner.py)
   │     │
   │     ├─► File Readers (readers.py) — CSV / JSON / Parquet Cell Stream
   │     │
   │     └─► Heuristic Engine (detectors.py)
   │           ├─ Email (RFC-compliant regex)
   │           ├─ SSN (Format + Range Rejection)
   │           ├─ Credit Card (Luhn Mod-10 Checksum)
   │           ├─ Phone (Word-bounded pattern)
   │           ├─ IP Address (IPv4 0-255 Octet Validation)
   │           └─ Date of Birth (Column-Name Heuristic + Format)
   │
   └─► Reporting Layer (reporter.py)
         ├─ Rich Terminal Panel & Table
         ├─ JSON Pipeline Stream
         └─ CSV Compliance Report
```

---

## 📊 Detection Capabilities & Validation

| PII Type | Verification Strategy | Accuracy / False Positive Defense |
|----------|----------------------|----------------------------------|
| **EMAIL** | RFC-compliant regex | 99% — Word boundary enforced |
| **SSN** | Format + Area exclusion | 98% — Rejects invalid 000, 666, 900+ ranges |
| **CREDIT_CARD** | Luhn Mod-10 Algorithm | 99% — Eliminates random 16-digit number false positives |
| **IP_ADDRESS** | IPv4 + Octet range check | 95% — Rejects 999.x.x.x and version strings |
| **PHONE** | US/International regex | 92% — Enforces strict `\b` word boundaries |
| **DATE_OF_BIRTH**| Format + Column Heuristics | 95% — Contextual matching (`dob`, `birth`, `bday`) |

---

## 🧪 Performance Benchmark

Run the reproducible benchmark script locally:

```bash
python examples/benchmark.py
```

- **Dataset**: 10,000 rows x 7 columns (70,000 cells)
- **Throughput**: ~45,000–60,000 cells/second
- **Memory Overhead**: Minimal (generator-based cell streaming)

---

## 🔧 CI/CD Integration

### GitHub Actions

```yaml
- name: Scan for PII before merge
  run: |
    pip install pii-radar
    pii-radar scan data/ --fail-on-detect --min-confidence 0.85
```

### Pre-commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: pii-radar
      name: PII Scanner
      entry: pii-radar scan
      args: [--fail-on-detect, --min-confidence, "0.9"]
      language: python
      types: [csv, json]
```

---

## 📁 Project Structure

```
pii-radar/
├── src/pii_radar/
│   ├── cli.py          ← Click CLI entry point (--sample, --fail-on-detect)
│   ├── scanner.py      ← Core scan orchestration with row limits
│   ├── detectors.py    ← Luhn + IPv4 range + DOB heuristics engine
│   ├── readers.py      ← CSV / JSON / Parquet readers
│   └── reporter.py     ← Rich terminal + JSON + CSV output
├── tests/
│   ├── conftest.py     ← Shared fixtures
│   ├── test_detectors.py
│   ├── test_negative_cases.py  ← False positive & Luhn unit tests
│   ├── test_scanner.py
│   └── test_cli.py
├── examples/
│   ├── sample.csv
│   ├── sample.json
│   └── benchmark.py    ← Performance benchmarking tool
├── .github/workflows/  ← CI/CD matrix (Ubuntu + Windows)
├── pyproject.toml
├── Makefile
└── README.md
```

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

## 👤 Author

**Nithin** · [github.com/nithin42](https://github.com/nithin42) · kumbam.nithingoud@gmail.com

> Part of an elite Data Science & Secure Computing portfolio.
> Focused on data privacy, reproducible ML, and secure systems engineering.
