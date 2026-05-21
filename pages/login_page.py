"""LoginPage: encapsulates all interactions with the SauceDemo login screen."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    # ── Selectors ──────────────────────────────────────────────────── #
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = "[data-test='error']"

    def __init__(self, page: Page, base_url: str) -> None:
        super().__init__(page)
        self.base_url = base_url

    # ── Actions ────────────────────────────────────────────────────── #

    def open(self) -> "LoginPage":
        self.navigate(self.base_url)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.fill(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.fill(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> "LoginPage":
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        """Convenience: fill both fields and submit."""
        return self.enter_username(username).enter_password(password).click_login()

    # ── Assertions / getters ───────────────────────────────────────── #

    def get_error_message(self) -> str:
        self.wait_for_selector(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)