"""InventoryPage: encapsulates all interactions on the SauceDemo inventory screen."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    # ── Selectors ──────────────────────────────────────────────────── #
    PAGE_TITLE = ".title"
    INVENTORY_ITEMS = ".inventory_item"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    ADD_TO_CART_BTN = "button[data-test^='add-to-cart']"
    ITEM_NAME = ".inventory_item_name"
    BURGER_MENU = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ────────────────────────────────────────────────────── #

    def add_first_item_to_cart(self) -> str:
        """Adds the first inventory item to the cart; returns the item name."""
        first_item = self.page.locator(self.INVENTORY_ITEMS).first
        item_name = first_item.locator(self.ITEM_NAME).inner_text()
        first_item.locator(self.ADD_TO_CART_BTN).click()
        return item_name

    def add_item_by_name(self, name: str) -> None:
        """Clicks 'Add to cart' for the item whose name matches *name*."""
        selector = f"button[data-test='add-to-cart-{name.lower().replace(' ', '-')}']"
        self.click(selector)

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)

    def logout(self) -> None:
        self.click(self.BURGER_MENU)
        self.page.wait_for_selector(self.LOGOUT_LINK)
        self.click(self.LOGOUT_LINK)

    # ── Getters ────────────────────────────────────────────────────── #

    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_cart_count(self) -> int:
        """Returns the numeric badge value; 0 if the badge is absent."""
        if not self.is_visible(self.CART_BADGE):
            return 0
        return int(self.get_text(self.CART_BADGE))

    def get_all_item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def is_on_inventory_page(self) -> bool:
        return "inventory" in self.get_current_url()