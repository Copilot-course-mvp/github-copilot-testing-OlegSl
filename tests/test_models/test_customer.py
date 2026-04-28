"""Unit tests for the Customer model."""
import pytest
from src.models.customer import Customer, CustomerTier


class TestCustomerCreation:
    """Tests for customer creation and validation."""

    def test_create_valid_customer(self):
        customer = Customer(
            id="C001",
            name="Alice Smith",
            email="alice@example.com",
        )
        assert customer.id == "C001"
        assert customer.name == "Alice Smith"
        assert customer.tier == CustomerTier.STANDARD

    def test_invalid_email_raises_error(self):
        with pytest.raises(ValueError, match="Invalid email"):
            Customer(id="C001", name="Alice", email="not-an-email")

    def test_empty_name_raises_error(self):
        with pytest.raises(ValueError, match="Customer name cannot be empty"):
            Customer(id="C001", name="", email="alice@example.com")

    def test_negative_total_spent_raises_error(self):
        with pytest.raises(ValueError, match="Total spent cannot be negative"):
            Customer(id="C001", name="Alice", email="alice@example.com", total_spent=-100.0)

    def test_negative_order_count_raises_error(self):
        with pytest.raises(ValueError, match="Order count cannot be negative"):
            Customer(id="C001", name="Alice", email="alice@example.com", order_count=-1)


class TestCustomerTierDiscount:
    """Tests for tier-based discounts."""

    def test_standard_tier_discount(self):
        customer = Customer(id="C001", name="Alice", email="alice@example.com")
        assert customer.tier_discount_percent == 0.0

    def test_silver_tier_discount(self):
        customer = Customer(
            id="C001", name="Alice", email="alice@example.com",
            tier=CustomerTier.SILVER
        )
        assert customer.tier_discount_percent == 5.0

    def test_gold_tier_discount(self):
        customer = Customer(
            id="C001", name="Alice", email="alice@example.com",
            tier=CustomerTier.GOLD
        )
        assert customer.tier_discount_percent == 10.0

    def test_platinum_tier_discount(self):
        customer = Customer(
            id="C001", name="Alice", email="alice@example.com",
            tier=CustomerTier.PLATINUM
        )
        assert customer.tier_discount_percent == 15.0


class TestCustomerTierUpdate:
    """Tests for automatic tier upgrades."""

    def test_tier_update_to_silver(self):
        customer = Customer(id="C001", name="Alice", email="alice@example.com", total_spent=1500)
        customer.update_tier()
        assert customer.tier == CustomerTier.SILVER

    def test_tier_update_to_gold(self):
        customer = Customer(id="C001", name="Alice", email="alice@example.com", total_spent=6000)
        customer.update_tier()
        assert customer.tier == CustomerTier.GOLD

    def test_tier_update_to_platinum(self):
        customer = Customer(id="C001", name="Alice", email="alice@example.com", total_spent=12000)
        customer.update_tier()
        assert customer.tier == CustomerTier.PLATINUM

    def test_record_purchase_updates_total_and_count(self):
        customer = Customer(id="C001", name="Alice", email="alice@example.com")
        customer.record_purchase(250.0)
        assert customer.total_spent == 250.0
        assert customer.order_count == 1

    def test_record_purchase_negative_raises_error(self):
        customer = Customer(id="C001", name="Alice", email="alice@example.com")
        with pytest.raises(ValueError, match="Purchase amount must be positive"):
            customer.record_purchase(-50.0)

    def test_tier_remains_standard_when_total_spent_under_threshold(self):
        customer = Customer(id="C001", name="Alice", email="alice@example.com", total_spent=999.0)
        customer.update_tier()
        assert customer.tier == CustomerTier.STANDARD

    def test_multiple_record_purchase_calls_accumulate_correctly(self):
        customer = Customer(id="C001", name="Alice", email="alice@example.com")
        customer.record_purchase(100.0)
        customer.record_purchase(200.0)

        assert customer.total_spent == 300.0
        assert customer.order_count == 2
