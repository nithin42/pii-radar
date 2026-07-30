# Quick Start Guide

## Installation

```bash
pip install pii-radar
```

## Basic Usage

### Scan a CSV file
```bash
pii-radar scan data/customers.csv
```

### Scan a JSON file
```bash
pii-radar scan logs/events.json
```

### Scan an entire directory
```bash
pii-radar scan data/
```

## Output Formats

### Terminal table (default)
```bash
pii-radar scan data.csv
```

### JSON output (for scripting)
```bash
pii-radar scan data.csv --output json
```

## Advanced Options

### Filter by confidence
```bash
pii-radar scan data.csv --min-confidence 0.9
```

### Save report to CSV
```bash
pii-radar scan data.csv --report pii_report.csv
```

### Create a redacted copy
```bash
pii-radar scan data.csv --redact data_clean.csv
```

### Fail build if PII found (CI/CD)
```bash
pii-radar scan data.csv --fail-on-detect
```

## Using as a Pre-commit Hook

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

## Using in GitHub Actions

```yaml
- name: Scan for PII
  run: |
    pip install pii-radar
    pii-radar scan data/ --fail-on-detect
```

## Support

Open an issue at https://github.com/nithin42/pii-radar/issues
