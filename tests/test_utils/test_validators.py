"""Unit tests for validator utilities."""
import pytest
from src.utils.validators import (
    validate_email,
    validate_price,
    validate_quantity,
    validate_product_id,
    validate_coupon_code,
    validate_customer_name,
)


class TestEmailValidator:
    """Tests for email validation."""

    def test_valid_email(self):
        assert validate_email("user@example.com") is True

    def test_valid_email_with_subdomain(self):
        assert validate_email("user@mail.example.co.uk") is True

    def test_missing_at_sign(self):
        assert validate_email("userexample.com") is False

    def test_missing_domain(self):
        assert validate_email("user@") is False

    def test_empty_string(self):
        assert validate_email("") is False

    def test_none_input_returns_false(self):
        assert validate_email(None) is False

    def test_email_with_spaces_is_invalid(self):
        assert validate_email("user @example.com") is False

    def test_email_with_special_characters_in_local_part(self):
        assert validate_email("user+test@example.com") is True


class TestPriceValidator:
    """Tests for price validation."""

    def test_valid_price_positive(self):
        assert validate_price(9.99) is True

    def test_valid_price_zero(self):
        assert validate_price(0.0) is True

    def test_invalid_price_negative(self):
        assert validate_price(-1.0) is False

    def test_string_input_returns_false(self):
        assert validate_price("9.99") is False

    def test_very_large_price_is_valid(self):
        assert validate_price(1e12) is True


class TestQuantityValidator:
    """Tests for quantity validation."""

    def test_valid_quantity(self):
        assert validate_quantity(5) is True

    def test_invalid_quantity_zero(self):
        assert validate_quantity(0) is False

    def test_invalid_quantity_negative(self):
        assert validate_quantity(-3) is False

    def test_float_input_returns_false(self):
        assert validate_quantity(1.5) is False

    def test_very_large_quantity_is_valid(self):
        assert validate_quantity(10**6) is True


class TestProductIdValidator:
    """Tests for product ID validation."""

    def test_valid_product_id(self):
        assert validate_product_id("P001") is True

    def test_valid_product_id_with_dashes(self):
        assert validate_product_id("PROD-001-XL") is True

    def test_empty_product_id(self):
        assert validate_product_id("") is False

    def test_product_id_starting_with_special_character_is_invalid(self):
        assert validate_product_id("@PROD001") is False

    def test_product_id_too_long_is_invalid(self):
        assert validate_product_id("A" * 51) is False
