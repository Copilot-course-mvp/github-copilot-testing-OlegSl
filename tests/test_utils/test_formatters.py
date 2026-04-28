"""Unit tests for formatter utilities."""
import pytest
from src.models.order import Order, OrderItem, OrderStatus
from src.models.customer import Customer, CustomerTier
from src.utils.formatters import (
    format_currency,
    format_order_summary,
    format_customer_info,
)


class TestFormatCurrency:
    """Tests for currency formatting."""

    def test_format_usd(self):
        assert format_currency(1234.56) == "$1,234.56"

    def test_format_usd_zero(self):
        assert format_currency(0.0) == "$0.00"

    def test_format_eur(self):
        assert format_currency(100.0, "EUR") == "€100.00"

    def test_format_gbp(self):
        assert format_currency(50.0, "GBP") == "£50.00"

    def test_unknown_currency_code(self):
        assert format_currency(1234.56, "JPY") == "1,234.56 JPY"

    def test_very_large_amount(self):
        assert format_currency(1000000.0) == "$1,000,000.00"


class TestFormatOrderSummary:
    """Tests for order summary formatting."""

    def test_summary_contains_order_id(self):
        order = Order(id="ORD-00001", customer_id="C001")
        summary = format_order_summary(order)
        assert "ORD-00001" in summary

    def test_summary_contains_status(self):
        order = Order(id="ORD-00001", customer_id="C001")
        summary = format_order_summary(order)
        assert "PENDING" in summary

    def test_discount_line_appears_when_discount_is_positive(self):
        order = Order(
            id="ORD-00001",
            customer_id="C001",
            discount_amount=5.0,
        )
        order.items.append(OrderItem(product_id="P001", product_name="Widget", quantity=1, unit_price=50.0))
        summary = format_order_summary(order)

        assert "Discount: -$5.00" in summary

    def test_shipping_line_appears_when_shipping_cost_is_positive(self):
        order = Order(
            id="ORD-00001",
            customer_id="C001",
            shipping_cost=9.99,
        )
        order.items.append(OrderItem(product_id="P001", product_name="Widget", quantity=1, unit_price=50.0))
        summary = format_order_summary(order)

        assert "Shipping: $9.99" in summary

    def test_summary_for_order_with_multiple_items(self):
        order = Order(id="ORD-00001", customer_id="C001")
        order.items.append(OrderItem(product_id="P001", product_name="Widget", quantity=1, unit_price=10.0))
        order.items.append(OrderItem(product_id="P002", product_name="Gadget", quantity=2, unit_price=20.0))
        summary = format_order_summary(order)

        assert "Items:    3" in summary


class TestFormatCustomerInfo:
    """Tests for customer info formatting."""

    def test_customer_info_contains_name(self):
        customer = Customer(id="C001", name="Alice Smith", email="alice@example.com")
        info = format_customer_info(customer)
        assert "Alice Smith" in info

    def test_customer_info_contains_email(self):
        customer = Customer(id="C001", name="Alice Smith", email="alice@example.com")
        info = format_customer_info(customer)
        assert "alice@example.com" in info

    def test_tier_is_shown_in_uppercase(self):
        customer = Customer(
            id="C001",
            name="Alice Smith",
            email="alice@example.com",
            tier=CustomerTier.SILVER,
        )
        info = format_customer_info(customer)

        assert "SILVER" in info

    def test_total_spent_is_formatted_as_currency(self):
        customer = Customer(
            id="C001",
            name="Alice Smith",
            email="alice@example.com",
            total_spent=1234.56,
        )
        info = format_customer_info(customer)

        assert "$1,234.56" in info
