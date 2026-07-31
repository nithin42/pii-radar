"""
Unit tests for negative cases and false-positive prevention.
"""

from __future__ import annotations

from pii_radar.detectors import detect, is_luhn_valid, is_valid_ipv4


class TestLuhnAlgorithm:
    def test_valid_luhn_credit_card(self):
        assert is_luhn_valid("4111111111111111")
        assert is_luhn_valid("4532015112830366")

    def test_invalid_luhn_number_rejected(self):
        assert not is_luhn_valid("4111111111111112")
        assert not is_luhn_valid("1234567890123456")

    def test_non_credit_card_length_rejected(self):
        assert not is_luhn_valid("123")
        assert not is_luhn_valid("123456789012345678901")


class TestIPv4Validation:
    def test_valid_ip(self):
        assert is_valid_ipv4("192.168.1.1")
        assert is_valid_ipv4("10.0.0.255")

    def test_invalid_octet_range_rejected(self):
        assert not is_valid_ipv4("999.999.999.999")
        assert not is_valid_ipv4("256.1.1.1")

    def test_version_strings_not_detected_as_ip(self):
        matches = detect("version 1.2.3", "version", 0)
        assert not any(m.pii_type == "IP_ADDRESS" for m in matches)


class TestDOBHeuristics:
    def test_dob_flagged_in_dob_column(self):
        matches = detect("03/15/1990", "patient_dob", 0)
        assert any(m.pii_type == "DATE_OF_BIRTH" for m in matches)

    def test_normal_date_ignored_in_non_dob_column(self):
        matches = detect("03/15/1990", "created_at", 0)
        assert not any(m.pii_type == "DATE_OF_BIRTH" for m in matches)

    def test_order_date_ignored(self):
        matches = detect("11/22/2024", "order_date", 0)
        assert not any(m.pii_type == "DATE_OF_BIRTH" for m in matches)


class TestCreditCardFalsePositives:
    def test_fake_16_digit_number_not_detected(self):
        matches = detect("1234567890123456", "account_id", 0)
        assert not any(m.pii_type == "CREDIT_CARD" for m in matches)
