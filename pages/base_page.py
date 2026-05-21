"""BasePage: shared low-level browser interactions for all page objects."""

from playwright.sync_api import Page, expect


class BasePage:
    """All page objects inherit from this class."""

    def __init__(self, page: Page) -> None:
        self.page = page

    # ------------------------------------------------------------------ #
    #  Navigation                                                          #
    # ------------------------------------------------------------------ #

    def navigate(self, url: str) -> None:
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    # ------------------------------------------------------------------ #
    #  Element helpers                                                     #
    # ------------------------------------------------------------------ #

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_for_selector(self, selector: str, timeout: int = 5000) -> None:
        self.page.wait_for_selector(selector, timeout=timeout)

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(lambda url: fragment in url)