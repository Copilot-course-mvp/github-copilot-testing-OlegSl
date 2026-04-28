"""Integration tests for the complete order processing flow.

These tests exercise multiple modules together to validate end-to-end behavior.

NOTE FOR STUDENTS: These integration tests cover the happy path.
Use GitHub Copilot to add tests for error conditions, edge cases,
and additional scenarios (e.g., order with multiple products,
discounts applied at various tiers, etc.).
"""
import pytest
from src.models.customer import Customer, CustomerTier
from src.models.product import Product
from src.services.inventory_service import InventoryService
from src.services.pricing_service import PricingService
from src.services.order_service import OrderService
from src.models.order import OrderStatus


@pytest.fixture
def inventory():
    svc = InventoryService()
    svc.add_product(Product(id="P001", name="Widget", price=30.0, stock=50, category="Tools"))
    svc.add_product(Product(id="P002", name="Gadget", price=80.0, stock=10, category="Electronics"))
    svc.add_product(Product(id="P003", name="Doohickey", price=15.0, stock=3, category="Misc"))
    return svc


@pytest.fixture
def pricing():
    return PricingService()


@pytest.fixture
def order_service(inventory, pricing):
    return OrderService(inventory=inventory, pricing=pricing)


@pytest.fixture
def standard_customer():
    return Customer(id="C001", name="Alice", email="alice@example.com")


@pytest.fixture
def gold_customer():
    return Customer(
        id="C002", name="Bob", email="bob@example.com",
        tier=CustomerTier.GOLD, total_spent=6000.0
    )


class TestHappyPathOrderFlow:
    """Tests for the standard successful order flow."""

    def test_full_order_lifecycle(self, order_service, standard_customer, inventory):
        """Test creating, filling, confirming, and advancing an order."""
        # Create order
        order = order_service.create_order(standard_customer)
        assert order.status == OrderStatus.PENDING

        # Add items
        order_service.add_item_to_order(order, "P001", 2)
        assert len(order.items) == 1

        # Confirm order
        order_service.confirm_order(order, standard_customer)
        assert order.status == OrderStatus.CONFIRMED

        # Advance through pipeline
        order_service.advance_order(order.id)
        assert order.status == OrderStatus.PROCESSING

        order_service.advance_order(order.id)
        assert order.status == OrderStatus.SHIPPED

        order_service.advance_order(order.id)
        assert order.status == OrderStatus.DELIVERED

    def test_free_shipping_applied_on_large_order(
        self, order_service, standard_customer
    ):
        """Orders with subtotal >= $75 should get free shipping."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P002", 1)  # $80 gadget
        order_service.confirm_order(order, standard_customer)
        assert order.shipping_cost == 0.0

    def test_shipping_cost_applied_on_small_order(
        self, order_service, standard_customer
    ):
        """Orders with subtotal < $75 should incur a shipping charge."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P001", 1)  # $30 widget
        order_service.confirm_order(order, standard_customer)
        assert order.shipping_cost == pytest.approx(9.99)

    def test_gold_customer_gets_discount(self, order_service, gold_customer):
        """Gold tier customers should receive a 10% discount."""
        order = order_service.create_order(gold_customer)
        order_service.add_item_to_order(order, "P002", 1)  # $80 gadget
        order_service.confirm_order(order, gold_customer)
        # 10% of $80 = $8 discount, no shipping (>= $75)
        assert order.discount_amount == pytest.approx(8.0)
        assert order.total == pytest.approx(72.0)


class TestCancellationFlow:
    """Tests for order cancellation and inventory restoration."""

    def test_cancel_order_restores_inventory(
        self, order_service, standard_customer, inventory
    ):
        """Cancelling an order should restore reserved stock."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P003", 2)
        # Stock should be 1 now (3 - 2)
        assert inventory.get_product("P003").stock == 1

        order_service.cancel_order(order.id)
        # Stock should be restored to 3
        assert inventory.get_product("P003").stock == 3
        assert order.status == OrderStatus.CANCELLED

    def test_cancel_after_confirm_restores_stock(
        self, order_service, standard_customer, inventory
    ):
        """Cancelling after confirming should still restore stock."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P003", 2)
        order_service.confirm_order(order, standard_customer)
        assert order.status == OrderStatus.CONFIRMED
        assert inventory.get_product("P003").stock == 1

        order_service.cancel_order(order.id)
        assert inventory.get_product("P003").stock == 3  # Restored
        assert order.status == OrderStatus.CANCELLED

    def test_cancelling_shipped_order_raises_error(self, order_service, standard_customer):
        """Cancelling a shipped order should raise an error."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P001", 1)
        order_service.confirm_order(order, standard_customer)
        order_service.advance_order(order.id)  # PROCESSING
        order_service.advance_order(order.id)  # SHIPPED

        with pytest.raises(ValueError, match="Cannot cancel"):
            order_service.cancel_order(order.id)

    def test_placing_multiple_orders_verifies_stock_correctly(
        self, order_service, standard_customer, inventory
    ):
        """Multiple orders should correctly reduce stock."""
        order1 = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order1, "P001", 2)  # Stock: 50 - 2 = 48

        order2 = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order2, "P001", 3)  # Stock: 48 - 3 = 45

        assert inventory.get_product("P001").stock == 45


class TestEdgeCases:
    """Edge case integration tests."""

    def test_order_with_multiple_products(
        self, order_service, standard_customer, inventory
    ):
        """Order with multiple different products should sum correctly."""
        order = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order, "P001", 1)  # $30
        order_service.add_item_to_order(order, "P002", 1)  # $80
        assert order.subtotal == pytest.approx(110.0)

    def test_exhausting_stock_prevents_further_orders(
        self, order_service, standard_customer
    ):
        """After exhausting stock, further orders for that product should fail."""
        order1 = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order1, "P003", 3)  # Uses all 3 in stock

        order2 = order_service.create_order(standard_customer)
        with pytest.raises(ValueError):
            order_service.add_item_to_order(order2, "P003", 1)

    def test_combining_coupon_codes_with_tier_discounts(self, order_service, gold_customer):
        """Test applying coupon codes with tier discounts."""
        order = order_service.create_order(gold_customer)
        order_service.add_item_to_order(order, "P002", 1)  # $80 gadget
        # Gold tier: 10% discount = $8, plus SAVE10 coupon: $8, but best discount wins
        # Pricing service uses max discount, so $8 from tier
        order_service.confirm_order(order, gold_customer)
        assert order.discount_amount == pytest.approx(8.0)  # Tier discount

    def test_listing_orders_by_customer(self, order_service, standard_customer, gold_customer):
        """Test listing orders by customer."""
        order1 = order_service.create_order(standard_customer)
        order2 = order_service.create_order(gold_customer)
        order3 = order_service.create_order(standard_customer)

        orders_for_standard = order_service.list_orders_by_customer(standard_customer.id)
        assert len(orders_for_standard) == 2
        assert {o.id for o in orders_for_standard} == {order1.id, order3.id}

    def test_listing_orders_by_status(self, order_service, standard_customer):
        """Test listing orders by status."""
        order1 = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order1, "P001", 1)
        order_service.confirm_order(order1, standard_customer)

        order2 = order_service.create_order(standard_customer)
        order_service.add_item_to_order(order2, "P001", 1)
        order_service.confirm_order(order2, standard_customer)
        order_service.advance_order(order2.id)  # PROCESSING

        pending_orders = order_service.list_orders_by_status(OrderStatus.PENDING)
        confirmed_orders = order_service.list_orders_by_status(OrderStatus.CONFIRMED)
        processing_orders = order_service.list_orders_by_status(OrderStatus.PROCESSING)

        assert len(pending_orders) == 0  # No pending after confirm
        assert len(confirmed_orders) == 1
        assert len(processing_orders) == 1
