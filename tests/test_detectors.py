"""Unit tests for pii_radar.detectors module."""

from __future__ import annotations

from pii_radar.detectors import detect, PIIMatch


class TestEmailDetection:
    def test_detects_standard_email(self):
        matches = detect("alice@example.com", "email_col", 0)
        types = [m.pii_type for m in matches]
        assert "EMAIL" in types

    def test_detects_email_in_sentence(self):
        matches = detect("Contact us at support@company.org today", "notes", 1)
        assert any(m.pii_type == "EMAIL" for m in matches)

    def test_no_false_positive_on_plain_text(self):
        matches = detect("hello world no email here", "text", 0)
        assert not any(m.pii_type == "EMAIL" for m in matches)

    def test_email_confidence_is_high(self):
        matches = detect("test@domain.com", "col", 0)
        email_matches = [m for m in matches if m.pii_type == "EMAIL"]
        assert email_matches[0].confidence >= 0.95

    def test_redacted_email_hides_local_part(self):
        matches = detect("alice@example.com", "col", 0)
        email_match = next(m for m in matches if m.pii_type == "EMAIL")
        assert "***" in email_match.value
        assert "@" in email_match.value


class TestPhoneDetection:
    def test_detects_us_phone_dashes(self):
        matches = detect("555-123-4567", "phone", 0)
        assert any(m.pii_type == "PHONE" for m in matches)

    def test_detects_us_phone_with_country_code(self):
        matches = detect("+1 (800) 555-9999", "contact", 0)
        assert any(m.pii_type == "PHONE" for m in matches)

    def test_no_false_positive_on_zip_code(self):
        matches = detect("12345", "zip", 0)
        assert not any(m.pii_type == "PHONE" for m in matches)


class TestSSNDetection:
    def test_detects_ssn_with_dashes(self):
        matches = detect("123-45-6789", "ssn_col", 0)
        assert any(m.pii_type == "SSN" for m in matches)

    def test_detects_ssn_with_spaces(self):
        matches = detect("234 56 7890", "col", 0)
        assert any(m.pii_type == "SSN" for m in matches)

    def test_rejects_invalid_ssn_000(self):
        matches = detect("000-45-6789", "col", 0)
        assert not any(m.pii_type == "SSN" for m in matches)


class TestIPDetection:
    def test_detects_valid_ipv4(self):
        matches = detect("192.168.1.100", "ip_address", 0)
        assert any(m.pii_type == "IP_ADDRESS" for m in matches)

    def test_no_false_positive_on_version(self):
        # "1.2.3" is not a full IP
        matches = detect("version 1.2.3", "version", 0)
        assert not any(m.pii_type == "IP_ADDRESS" for m in matches)


class TestCreditCardDetection:
    def test_detects_visa(self):
        matches = detect("4111111111111111", "card", 0)
        assert any(m.pii_type == "CREDIT_CARD" for m in matches)


class TestPIIMatchDataclass:
    def test_pii_match_repr(self):
        m = PIIMatch("EMAIL", "al***@ex.com", 0.98, "email_col", 3)
        assert "EMAIL" in repr(m)
        assert "email_col" in repr(m)

    def test_empty_string_returns_no_matches(self):
        assert detect("", "col", 0) == []

    def test_whitespace_returns_no_matches(self):
        assert detect("   ", "col", 0) == []

    def test_none_type_returns_no_matches(self):
        assert detect(None, "col", 0) == []  # type: ignore[arg-type]
