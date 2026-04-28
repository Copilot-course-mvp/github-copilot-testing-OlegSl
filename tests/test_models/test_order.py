"""Unit tests for the Order and OrderItem models."""
import pytest
from src.models.order import Order, OrderItem, OrderStatus


def make_item(product_id="P001", name="Widget", quantity=2, unit_price=10.0):
    return OrderItem(
        product_id=product_id,
        product_name=name,
        quantity=quantity,
        unit_price=unit_price,
    )


class TestOrderItem:
    """Tests for the OrderItem model."""

    def test_subtotal_calculation(self):
        item = make_item(quantity=3, unit_price=15.0)
        assert item.subtotal == 45.0

    def test_zero_quantity_raises_error(self):
        with pytest.raises(ValueError, match="Quantity must be positive"):
            OrderItem(product_id="P1", product_name="X", quantity=0, unit_price=10.0)

    def test_negative_unit_price_raises_error(self):
        with pytest.raises(ValueError, match="Unit price cannot be negative"):
            OrderItem(product_id="P1", product_name="X", quantity=1, unit_price=-5.0)

    def test_subtotal_with_zero_unit_price(self):
        item = make_item(quantity=2, unit_price=0.0)
        assert item.subtotal == 0.0


class TestOrderSubtotalAndTotal:
    """Tests for order financial calculations."""

    def test_empty_order_subtotal(self):
        order = Order(id="O001", customer_id="C001")
        assert order.subtotal == 0.0

    def test_subtotal_with_items(self):
        order = Order(id="O001", customer_id="C001")
        order.items.append(make_item(quantity=2, unit_price=10.0))
        order.items.append(make_item(quantity=1, unit_price=25.0))
        assert order.subtotal == 45.0

    def test_total_includes_shipping(self):
        order = Order(id="O001", customer_id="C001", shipping_cost=9.99)
        order.items.append(make_item(quantity=1, unit_price=50.0))
        assert order.total == pytest.approx(59.99)

    def test_total_applies_discount(self):
        order = Order(id="O001", customer_id="C001", discount_amount=5.0)
        order.items.append(make_item(quantity=1, unit_price=50.0))
        assert order.total == 45.0

    def test_total_never_goes_below_zero(self):
        order = Order(id="O001", customer_id="C001", discount_amount=100.0)
        order.items.append(make_item(quantity=1, unit_price=50.0))
        assert order.total == 0.0

    def test_item_count_sums_all_quantities(self):
        order = Order(id="O001", customer_id="C001")
        order.items.append(make_item(quantity=2, unit_price=10.0))
        order.items.append(make_item(quantity=3, unit_price=15.0))
        assert order.item_count == 5


class TestOrderStatusTransitions:
    """Tests for order lifecycle state machine."""

    def test_new_order_is_pending(self):
        order = Order(id="O001", customer_id="C001")
        assert order.status == OrderStatus.PENDING

    def test_confirm_pending_order(self):
        order = Order(id="O001", customer_id="C001")
        order.items.append(make_item())
        order.confirm()
        assert order.status == OrderStatus.CONFIRMED

    def test_confirm_empty_order_raises_error(self):
        order = Order(id="O001", customer_id="C001")
        with pytest.raises(ValueError, match="Cannot confirm an empty order"):
            order.confirm()

    def test_cancel_pending_order(self):
        order = Order(id="O001", customer_id="C001")
        order.cancel()
        assert order.status == OrderStatus.CANCELLED

    def test_cancel_shipped_order_raises_error(self):
        order = Order(id="O001", customer_id="C001", status=OrderStatus.SHIPPED)
        with pytest.raises(ValueError, match="Cannot cancel"):
            order.cancel()

    def test_advance_status_from_confirmed(self):
        order = Order(id="O001", customer_id="C001", status=OrderStatus.CONFIRMED)
        order.advance_status()
        assert order.status == OrderStatus.PROCESSING

    def test_advance_status_from_processing_to_shipped(self):
        order = Order(id="O001", customer_id="C001", status=OrderStatus.PROCESSING)
        order.advance_status()
        assert order.status == OrderStatus.SHIPPED

    def test_advance_status_from_shipped_to_delivered(self):
        order = Order(id="O001", customer_id="C001", status=OrderStatus.SHIPPED)
        order.advance_status()
        assert order.status == OrderStatus.DELIVERED

    def test_advance_status_on_cancelled_raises_value_error(self):
        order = Order(id="O001", customer_id="C001", status=OrderStatus.CANCELLED)
        with pytest.raises(ValueError, match="Cannot advance order"):
            order.advance_status()

    def test_add_item_on_non_pending_order_raises_value_error(self):
        order = Order(id="O001", customer_id="C001", status=OrderStatus.CONFIRMED)
        with pytest.raises(ValueError, match="Cannot add items"):
            order.add_item(make_item())
