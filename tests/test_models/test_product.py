"""Unit tests for the Product model.

NOTE FOR STUDENTS: Several test cases are missing from this file.
Use GitHub Copilot to identify and fill in the gaps.
"""
import pytest
from src.models.product import Product


class TestProductCreation:
    """Tests for product creation and validation."""

    def test_create_valid_product(self):
        product = Product(
            id="P001",
            name="Laptop",
            price=999.99,
            stock=10,
            category="Electronics",
        )
        assert product.id == "P001"
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.stock == 10
        assert product.category == "Electronics"

    def test_create_product_with_description(self):
        product = Product(
            id="P002",
            name="Phone",
            price=499.99,
            stock=5,
            category="Electronics",
            description="A great smartphone",
        )
        assert product.description == "A great smartphone"

    def test_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            Product(id="P001", name="Item", price=-1.0, stock=5, category="General")

    def test_negative_stock_raises_error(self):
        with pytest.raises(ValueError, match="Stock cannot be negative"):
            Product(id="P001", name="Item", price=10.0, stock=-1, category="General")

    def test_empty_name_raises_error(self):
        with pytest.raises(ValueError, match="Product name cannot be empty"):
            Product(id="P001", name="", price=10.0, stock=5, category="General")

    def test_discount_percent_above_100_raises_error(self):
        with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
            Product(id="P001", name="Item", price=10.0, stock=5, category="General", discount_percent=150.0)

    def test_discount_percent_below_zero_raises_error(self):
        with pytest.raises(ValueError, match="Discount percent must be between 0 and 100"):
            Product(id="P001", name="Item", price=10.0, stock=5, category="General", discount_percent=-5.0)


class TestProductProperties:
    """Tests for product computed properties."""

    def test_discounted_price_with_no_discount(self):
        product = Product(id="P001", name="Item", price=100.0, stock=5, category="X")
        assert product.discounted_price == 100.0

    def test_discounted_price_with_discount(self):
        product = Product(
            id="P001", name="Item", price=100.0, stock=5, category="X",
            discount_percent=20.0
        )
        assert product.discounted_price == 80.0

    def test_is_available_when_in_stock(self):
        product = Product(id="P001", name="Item", price=10.0, stock=3, category="X")
        assert product.is_available is True

    def test_is_available_when_stock_is_zero(self):
        product = Product(id="P001", name="Item", price=10.0, stock=0, category="X")
        assert product.is_available is False


class TestProductStockManagement:
    """Tests for stock reduction and restocking."""

    def test_reduce_stock_successfully(self):
        product = Product(id="P001", name="Item", price=10.0, stock=10, category="X")
        product.reduce_stock(3)
        assert product.stock == 7

    def test_reduce_stock_to_zero(self):
        product = Product(id="P001", name="Item", price=10.0, stock=5, category="X")
        product.reduce_stock(5)
        assert product.stock == 0

    def test_reduce_stock_insufficient_raises_error(self):
        product = Product(id="P001", name="Item", price=10.0, stock=3, category="X")
        with pytest.raises(ValueError, match="Insufficient stock"):
            product.reduce_stock(10)

    def test_reduce_stock_zero_quantity_raises_error(self):
        product = Product(id="P001", name="Item", price=10.0, stock=5, category="X")
        with pytest.raises(ValueError, match="Quantity must be positive"):
            product.reduce_stock(0)

    def test_restock_product(self):
        product = Product(id="P001", name="Item", price=10.0, stock=5, category="X")
        product.restock(10)
        assert product.stock == 15

    def test_restock_with_zero_quantity_raises_error(self):
        product = Product(id="P001", name="Item", price=10.0, stock=5, category="X")
        with pytest.raises(ValueError, match="Quantity must be positive"):
            product.restock(0)

    def test_restock_with_negative_quantity_raises_error(self):
        product = Product(id="P001", name="Item", price=10.0, stock=5, category="X")
        with pytest.raises(ValueError, match="Quantity must be positive"):
            product.restock(-3)

    def test_product_repr(self):
        product = Product(id="P001", name="Laptop", price=999.99, stock=10, category="Electronics")
        assert repr(product) == "Product(id='P001', name='Laptop', price=999.99, stock=10)"
