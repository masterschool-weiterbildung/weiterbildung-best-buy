import pytest

import products
import store


@pytest.fixture
def setup_data():
    """
    Fixture to set up test data for store and products.

    Creates a list of sample products and initializes a store with these products.
    Yields the store instance to the test functions and performs teardown after tests complete.

    Returns:
        Store: An instance of the Store class with preloaded products.
    """
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250,
                         quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250)
    ]

    best_buy = store.Store(product_list)
    print("\nSetting up resources...")
    yield best_buy  # Provide the data to the test
    # Teardown: Clean up resources (if any) after the test
    print("\nTearing down resources...")


class TestPRODUCT:
    """
    Test suite for Product-related functionality, including
    product creation, validation, quantity, and purchasing logic.
    """

    @pytest.mark.parametrize("product",
                             [
                                 products.Product("MacBook Air M2",
                                                  price=1450, quantity=100)
                             ]
                             )
    def test_create_products(self, product, setup_data):
        """
        Test product creation.

        Asserts that the created product in setup matches the expected product instance.

        Parameters:
            product (Product): Product instance to test.
            setup_data (Store): The store instance with preloaded products.
        """
        assert setup_data.get_all_products()[0] == product

    def test_create_product_with_invalid_details_negative_quantity(self,
                                                                   setup_data):
        """
        Test creation of product with a negative quantity.

        Expects a ValueError when attempting to set a negative quantity.

        Parameter:
            setup_data (Store): The store instance with products.
        """
        with pytest.raises(ValueError,
                           match="Quantity must be a int"):
            setup_data.get_products()[0].set_quantity(-10000)

    def test_create_product_with_invalid_details_empty_quantity(self,
                                                                setup_data):
        """
        Test creation of product with empty quantity.

        Expects a ValueError when attempting to set an empty quantity.

        Parameter:
            setup_data (Store): The store instance with products.
        """
        with pytest.raises(ValueError,
                           match="Quantity must be a int"):
            setup_data.get_products()[0].set_quantity("")

    def test_create_product_with_invalid_details_negative_price(self,
                                                                setup_data):
        """
        Test creation of product with a negative price.

        Expects a ValueError when attempting to set a negative price.

        Parameter:
            setup_data (Store): The store instance with products.
        """
        with pytest.raises(ValueError,
                           match="Price must be a float"):
            setup_data.get_products()[0].set_price(-10000)

    def test_create_product_with_invalid_details_empty_price(self,
                                                             setup_data):
        """
        Test creation of product with empty price.

        Expects a ValueError when attempting to set an empty price.

        Parameter:
            setup_data (Store): The store instance with products.
        """
        with pytest.raises(ValueError,
                           match="Price must be a float"):
            setup_data.get_products()[0].set_price("")

    @pytest.mark.parametrize("product",
                             [
                                 products.Product("MacBook Air M2",
                                                  price=1450, quantity=100)
                             ]
                             )
    def test_product_reaches_zero_quantity(self, product, setup_data):
        """
        Test that product is removed from store inventory when quantity reaches zero.

        Sets product quantity to zero and asserts that it no longer exists in the store's inventory.

        Parameters:
            product (Product): The product instance to test.
            setup_data (Store): The store instance with products.
        """
        setup_data.get_all_products()[0].set_quantity(0)
        assert product not in setup_data.get_all_products()

    def test_product_purchase_check_final_quantity(self, setup_data):
        """
        Test product quantity after a purchase.

        Reduces the quantity of a product by 50 and asserts the new quantity is correct.

        Parameter:
            setup_data (Store): The store instance with products.
        """
        (setup_data.get_all_products()[0]
         .set_quantity(setup_data.get_all_products()[0].get_quantity() - 50))
        assert setup_data.get_all_products()[0].get_quantity() == 50

    @pytest.mark.parametrize("product",
                             [
                                 products.Product("MacBook Air M2",
                                                  price=1450, quantity=100)
                             ]
                             )
    def test_buying_larger_quantities(self, product, setup_data):
        """
        Test purchasing quantity exceeding available stock.

        Expects a ValueError when attempting to purchase a quantity greater than available stock.

        Parameters:
            product (Product): The product instance to test.
            setup_data (Store): The store instance with products.
        """
        with pytest.raises(ValueError,
                           match="Error while making order! Quantity larger "
                                 "than what exists\n"):
            setup_data.validate_order([(product, 101)])