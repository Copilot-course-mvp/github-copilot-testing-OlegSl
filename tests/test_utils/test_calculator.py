"""Unit tests for calculator utilities."""
import pytest
from src.utils.calculator import (
    calculate_tax,
    calculate_average,
    calculate_percentage_change,
    calculate_compound_interest,
    apply_discount,
)


class TestCalculateTax:
    """Tests for tax calculation."""

    def test_tax_calculation_basic(self):
        assert calculate_tax(100.0, 10.0) == 10.0

    def test_tax_calculation_zero_rate(self):
        assert calculate_tax(100.0, 0.0) == 0.0

    def test_tax_calculation_zero_amount(self):
        assert calculate_tax(0.0, 8.5) == 0.0

    def test_negative_amount_raises_error(self):
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            calculate_tax(-50.0, 10.0)

    def test_tax_rate_over_100_raises_error(self):
        with pytest.raises(ValueError, match="Tax rate must be between"):
            calculate_tax(100.0, 101.0)

    def test_fractional_tax_rate(self):
        assert calculate_tax(100.0, 8.75) == pytest.approx(8.75)

    def test_negative_tax_rate_raises_value_error(self):
        with pytest.raises(ValueError, match="Tax rate must be between"):
            calculate_tax(100.0, -5.0)

    def test_hundred_percent_tax_rate(self):
        assert calculate_tax(100.0, 100.0) == 100.0


class TestCalculateAverage:
    """Tests for average calculation."""

    def test_average_of_list(self):
        assert calculate_average([1.0, 2.0, 3.0]) == 2.0

    def test_average_of_single_value(self):
        assert calculate_average([42.0]) == 42.0

    def test_average_of_empty_list(self):
        assert calculate_average([]) is None

    def test_average_of_list_with_negative_values(self):
        assert calculate_average([-1.0, 1.0, 2.0]) == pytest.approx(0.6666666666666666)

    def test_average_of_large_list(self):
        values = list(range(1000))
        assert calculate_average(values) == pytest.approx(499.5)


class TestCalculatePercentageChange:
    """Tests for percentage change calculation."""

    def test_positive_change(self):
        assert calculate_percentage_change(100.0, 120.0) == pytest.approx(20.0)

    def test_negative_change(self):
        assert calculate_percentage_change(100.0, 80.0) == pytest.approx(-20.0)

    def test_no_change(self):
        assert calculate_percentage_change(100.0, 100.0) == pytest.approx(0.0)

    def test_zero_old_value_raises_error(self):
        with pytest.raises(ValueError, match="Cannot calculate percentage change from zero"):
            calculate_percentage_change(0.0, 50.0)

    def test_change_from_negative_value(self):
        assert calculate_percentage_change(-50.0, 50.0) == pytest.approx(200.0)


class TestApplyDiscount:
    """Tests for discount application."""

    def test_apply_twenty_percent_discount(self):
        assert apply_discount(100.0, 20.0) == 80.0

    def test_apply_zero_discount(self):
        assert apply_discount(100.0, 0.0) == 100.0

    def test_apply_full_discount(self):
        assert apply_discount(100.0, 100.0) == 0.0

    def test_negative_amount_raises_error(self):
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            apply_discount(-10.0, 10.0)

    def test_discount_greater_than_100_raises_value_error(self):
        with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
            apply_discount(100.0, 150.0)

    def test_discount_less_than_zero_raises_value_error(self):
        with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
            apply_discount(100.0, -5.0)


class TestCompoundInterest:
    """Tests for compound interest calculation."""

    def test_compound_interest_basic(self):
        # 1000 at 10% for 1 period = 1100
        assert calculate_compound_interest(1000.0, 10.0, 1) == pytest.approx(1100.0)

    def test_compound_interest_zero_periods(self):
        assert calculate_compound_interest(1000.0, 10.0, 0) == pytest.approx(1000.0)

    def test_negative_principal_raises_value_error(self):
        with pytest.raises(ValueError, match="Principal cannot be negative"):
            calculate_compound_interest(-1000.0, 10.0, 1)

    def test_negative_rate_raises_value_error(self):
        with pytest.raises(ValueError, match="Rate cannot be negative"):
            calculate_compound_interest(1000.0, -5.0, 1)

    def test_compound_interest_multiple_periods(self):
        assert calculate_compound_interest(1000.0, 10.0, 2) == pytest.approx(1210.0)

    def test_calculate_compound_interest_negative_periods_raises_value_error(self):
        with pytest.raises(ValueError, match="Periods cannot be negative"):
            calculate_compound_interest(1000.0, 10.0, -1)
