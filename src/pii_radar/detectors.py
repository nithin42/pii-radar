"""
PII pattern detectors using regex and heuristics.

Supports detection of:
- Email addresses
- Phone numbers (US/international)
- Social Security Numbers (SSN)
- Credit card numbers
- IP addresses (v4 and v6)
- Dates of birth
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class PIIMatch:
    """Represents a single PII detection result."""

    pii_type: str
    value: str
    confidence: float  # 0.0 to 1.0
    column: str
    row_index: int

    def __repr__(self) -> str:
        return (
            f"PIIMatch(type={self.pii_type!r}, column={self.column!r}, "
            f"row={self.row_index}, confidence={self.confidence:.0%})"
        )


# ---------------------------------------------------------------------------
# Compiled regex patterns
# ---------------------------------------------------------------------------

_PATTERNS: dict[str, tuple[re.Pattern, float]] = {
    "EMAIL": (
        re.compile(
            r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
        0.98,
    ),
    "PHONE": (
        re.compile(
            r"""
            (?:
                (?:\+?1[\s\-.])?          # optional country code
                (?:\(?\d{3}\)?[\s\-.]?)   # area code
                \d{3}[\s\-.]              # prefix
                \d{4}                     # line number
            )
            """,
            re.VERBOSE,
        ),
        0.85,
    ),
    "SSN": (
        re.compile(
            r"\b(?!000|666|9\d{2})\d{3}[- ](?!00)\d{2}[- ](?!0{4})\d{4}\b"
        ),
        0.97,
    ),
    "CREDIT_CARD": (
        re.compile(
            r"""
            \b
            (?:
                4[0-9]{12}(?:[0-9]{3})?       |  # Visa
                5[1-5][0-9]{14}               |  # MasterCard
                3[47][0-9]{13}                |  # Amex
                3(?:0[0-5]|[68][0-9])[0-9]{11}|  # Diners
                6(?:011|5[0-9]{2})[0-9]{12}   |  # Discover
                (?:2131|1800|35\d{3})\d{11}      # JCB
            )
            \b
            """,
            re.VERBOSE,
        ),
        0.92,
    ),
    "IP_ADDRESS": (
        re.compile(
            r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"
        ),
        0.90,
    ),
    "DATE_OF_BIRTH": (
        re.compile(
            r"\b(?:0?[1-9]|1[0-2])[/\-.](?:0?[1-9]|[12]\d|3[01])[/\-.]"
            r"(?:19|20)\d{2}\b"
        ),
        0.75,
    ),
}


def detect(value: str, column: str, row_index: int) -> List[PIIMatch]:
    """
    Scan a single string value for PII patterns.

    Args:
        value: The string to scan.
        column: The column name the value came from.
        row_index: The row index in the dataset.

    Returns:
        List of PIIMatch objects, one per detected PII type.
    """
    if not isinstance(value, str) or not value.strip():
        return []

    matches: List[PIIMatch] = []
    for pii_type, (pattern, confidence) in _PATTERNS.items():
        if pattern.search(value):
            matches.append(
                PIIMatch(
                    pii_type=pii_type,
                    value=_redact_value(value, pii_type),
                    confidence=confidence,
                    column=column,
                    row_index=row_index,
                )
            )
    return matches


def _redact_value(value: str, pii_type: str) -> str:
    """Return a partially redacted version of the value for safe reporting."""
    if len(value) <= 4:
        return "****"
    if pii_type == "EMAIL":
        parts = value.split("@")
        return f"{parts[0][:2]}***@{parts[1]}" if len(parts) == 2 else "****"
    if pii_type in ("CREDIT_CARD", "SSN"):
        return f"{'*' * (len(value) - 4)}{value[-4:]}"
    return f"{value[:2]}{'*' * (len(value) - 4)}{value[-2:]}"

# SSN validation: rejects area numbers 000, 666, and 900-999
