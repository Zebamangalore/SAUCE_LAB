"""test_login_success.py – verifies the happy-path login flow."""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
@pytest.mark.login
def test_successful_login(login_page: LoginPage, valid_creds: dict):
    """
    GIVEN  valid SauceDemo credentials
    WHEN   the user submits the login form
    THEN   the browser lands on the inventory page
    AND    the page title reads 'Products'
    """
    login_page.open().login(
        username=valid_creds["username"],
        password=valid_creds["password"],
    )

    # Verify redirect to inventory
    assert "inventory" in login_page.get_current_url(), (
        f"Expected URL to contain 'inventory', got: {login_page.get_current_url()}"
    )

    # Verify page heading
    inventory = InventoryPage(login_page.page)
    assert inventory.get_page_title() == "Products", (
        f"Expected page title 'Products', got: '{inventory.get_page_title()}'"
    )