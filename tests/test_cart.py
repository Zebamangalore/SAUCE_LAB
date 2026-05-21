"""test_cart.py – verifies adding items to the cart and badge count."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture
def logged_in_inventory(login_page: LoginPage, valid_creds: dict) -> InventoryPage:
    """Helper fixture: performs login and returns an InventoryPage instance."""
    login_page.open().login(
        username=valid_creds["username"],
        password=valid_creds["password"],
    )
    return InventoryPage(login_page.page)


@pytest.mark.smoke
@pytest.mark.cart
def test_add_single_item_increments_cart_badge(logged_in_inventory: InventoryPage):
    """
    GIVEN  the user is on the inventory page
    WHEN   they click 'Add to cart' for the first product
    THEN   the cart badge shows a count of 1
    """
    assert logged_in_inventory.get_cart_count() == 0, (
        "Cart should be empty before adding any item"
    )

    item_name = logged_in_inventory.add_first_item_to_cart()

    assert logged_in_inventory.get_cart_count() == 1, (
        f"Cart badge should show 1 after adding '{item_name}'"
    )


@pytest.mark.regression
@pytest.mark.cart
def test_add_multiple_items_updates_cart_count(logged_in_inventory: InventoryPage):
    """
    GIVEN  the user is on the inventory page
    WHEN   they add two distinct products to the cart
    THEN   the cart badge shows a count of 2
    """
    logged_in_inventory.add_first_item_to_cart()

    # Add a second item (second inventory entry)
    second_item = logged_in_inventory.page.locator(".inventory_item").nth(1)
    second_item.locator("button[data-test^='add-to-cart']").click()

    assert logged_in_inventory.get_cart_count() == 2, (
        "Cart badge should show 2 after adding two items"
    )


@pytest.mark.smoke
@pytest.mark.cart
def test_cart_count_persists_after_navigation(logged_in_inventory: InventoryPage):
    """
    GIVEN  the user has added one item
    WHEN   they navigate to the cart page and return to inventory
    THEN   the cart badge still shows 1
    """
    logged_in_inventory.add_first_item_to_cart()
    logged_in_inventory.go_to_cart()

    # Navigate back to inventory
    logged_in_inventory.page.go_back()

    assert logged_in_inventory.get_cart_count() == 1, (
        "Cart count should persist after navigating away and back"
    )