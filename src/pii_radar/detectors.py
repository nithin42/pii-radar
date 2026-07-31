"""
PII pattern detectors with heuristic and cryptographic validation.

Supports detection of:
- Email addresses (RFC-compliant regex)
- Phone numbers (US/international with strict word boundaries)
- Social Security Numbers (SSN, format + invalid range rejection)
- Credit card numbers (Luhn Mod-10 algorithm validation)
- IP addresses (IPv4 with octet range validation 0-255)
- Dates of Birth (format + column name context heuristics)
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

_EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
    re.IGNORECASE,
)

_PHONE_PATTERN = re.compile(
    r"\b(?:(?:\+?1[\s\-.]?)?(?:\(\d{3}\)|\d{3})[\s\-.]?\d{3}[\s\-.]?\d{4})\b"
)

_SSN_PATTERN = re.compile(
    r"\b(?!000|666|9\d{2})\d{3}[- ](?!00)\d{2}[- ](?!0{4})\d{4}\b"
)

_CREDIT_CARD_RAW_PATTERN = re.compile(
    r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
)

_DOB_DATE_PATTERN = re.compile(
    r"\b(?:0?[1-9]|1[0-2])[/\-.](?:0?[1-9]|[12]\d|3[01])[/\-.](?:19|20)\d{2}\b"
)

_IPV4_PATTERN = re.compile(
    r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
)

PATTERNS = {
    "EMAIL": _EMAIL_PATTERN,
    "PHONE": _PHONE_PATTERN,
    "SSN": _SSN_PATTERN,
    "CREDIT_CARD": _CREDIT_CARD_RAW_PATTERN,
    "IP_ADDRESS": _IPV4_PATTERN,
    "DATE_OF_BIRTH": _DOB_DATE_PATTERN,
}

_DOB_COLUMN_KEYWORDS = {
    "dob", "birth", "birthday", "date_of_birth", "born", "birthdate", "bday"
}

_EMAIL_COLUMN_KEYWORDS = {"email", "e_mail", "mail", "email_address"}
_PHONE_COLUMN_KEYWORDS = {"phone", "telephone", "mobile", "cell", "contact_no", "phone_number"}
_SSN_COLUMN_KEYWORDS = {"ssn", "social_security", "tax_id", "national_id"}
_CARD_COLUMN_KEYWORDS = {"card", "credit_card", "cc_num", "pan", "card_number"}


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def is_luhn_valid(card_number: str) -> bool:
    """
    Validate a credit card number using Luhn Mod-10 algorithm.

    Args:
        card_number: Digits string (hyphens/spaces removed).

    Returns:
        True if the number satisfies Luhn algorithm, False otherwise.
    """
    digits = [int(c) for c in card_number if c.isdigit()]
    if len(digits) < 13 or len(digits) > 19:
        return False
    checksum = 0
    reverse_digits = digits[::-1]
    for idx, digit in enumerate(reverse_digits):
        if idx % 2 == 1:
            doubled = digit * 2
            checksum += doubled - 9 if doubled > 9 else doubled
        else:
            checksum += digit
    return checksum % 10 == 0


def is_valid_ipv4(ip_str: str) -> bool:
    """
    Validate IPv4 octet ranges (0-255 per octet) and reject invalid IPs/versions.
    """
    octets = ip_str.split(".")
    if len(octets) != 4:
        return False
    try:
        numbers = [int(o) for o in octets]
        if any(n < 0 or n > 255 for n in numbers):
            return False
        # Reject 0.0.0.0 or loopback/local ranges if desired, but 0-255 is primary check
        return True
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Main detection function
# ---------------------------------------------------------------------------

def detect(value: str, column: str, row_index: int) -> List[PIIMatch]:
    """
    Scan a single string value for PII patterns with heuristic validation.

    Args:
        value: The string to scan.
        column: The column name the value came from.
        row_index: The row index in the dataset.

    Returns:
        List of PIIMatch objects, one per detected PII type.
    """
    if not isinstance(value, str) or not value.strip():
        return []

    val_clean = value.strip()
    col_lower = column.lower()
    matches: List[PIIMatch] = []

    # 1. Email Detection
    if _EMAIL_PATTERN.search(val_clean):
        confidence = 0.99 if any(k in col_lower for k in _EMAIL_COLUMN_KEYWORDS) else 0.98
        matches.append(
            PIIMatch(
                pii_type="EMAIL",
                value=_redact_value(val_clean, "EMAIL"),
                confidence=confidence,
                column=column,
                row_index=row_index,
            )
        )

    # 2. SSN Detection
    if _SSN_PATTERN.search(val_clean):
        confidence = 0.99 if any(k in col_lower for k in _SSN_COLUMN_KEYWORDS) else 0.97
        matches.append(
            PIIMatch(
                pii_type="SSN",
                value=_redact_value(val_clean, "SSN"),
                confidence=confidence,
                column=column,
                row_index=row_index,
            )
        )

    # 3. Credit Card Detection (Raw regex + Luhn validation)
    cc_match = _CREDIT_CARD_RAW_PATTERN.search(val_clean)
    if cc_match:
        raw_digits = re.sub(r"\D", "", cc_match.group(0))
        if is_luhn_valid(raw_digits):
            confidence = 0.99 if any(k in col_lower for k in _CARD_COLUMN_KEYWORDS) else 0.95
            matches.append(
                PIIMatch(
                    pii_type="CREDIT_CARD",
                    value=_redact_value(val_clean, "CREDIT_CARD"),
                    confidence=confidence,
                    column=column,
                    row_index=row_index,
                )
            )

    # 4. Phone Detection
    if _PHONE_PATTERN.search(val_clean):
        confidence = 0.95 if any(k in col_lower for k in _PHONE_COLUMN_KEYWORDS) else 0.85
        matches.append(
            PIIMatch(
                pii_type="PHONE",
                value=_redact_value(val_clean, "PHONE"),
                confidence=confidence,
                column=column,
                row_index=row_index,
            )
        )

    # 5. IP Address Detection (Regex + IPv4 range check)
    ip_match = _IPV4_PATTERN.search(val_clean)
    if ip_match and is_valid_ipv4(ip_match.group(0)):
        matches.append(
            PIIMatch(
                pii_type="IP_ADDRESS",
                value=_redact_value(val_clean, "IP_ADDRESS"),
                confidence=0.90,
                column=column,
                row_index=row_index,
            )
        )

    # 6. Date of Birth (Format + Column Keyword Heuristics)
    if _DOB_DATE_PATTERN.search(val_clean):
        is_dob_col = any(k in col_lower for k in _DOB_COLUMN_KEYWORDS)
        # Only flag if column name suggests DOB, or assign lower confidence
        if is_dob_col:
            matches.append(
                PIIMatch(
                    pii_type="DATE_OF_BIRTH",
                    value=_redact_value(val_clean, "DATE_OF_BIRTH"),
                    confidence=0.92,
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
