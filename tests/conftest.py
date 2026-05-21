"""conftest.py – shared fixtures for the SauceDemo POM test suite.

We override pytest-playwright's `browser_type_launch_args` fixture so that
HEADLESS and SLOWMO values in .env / environment are respected.

Run headed + slow locally:
    # In .env:  HEADLESS=false  SLOWMO=800
    pytest --browser chromium

Run both browsers (CI matrix style):
    pytest --browser chromium --browser firefox
"""

import pytest
from typing import Any, Dict
from faker import Faker
from playwright.sync_api import Page

from config import config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


# ──────────────────────────────────────────────────────────────────────────── #
#  Override launch args: HEADLESS + SLOWMO from .env                           #
# ──────────────────────────────────────────────────────────────────────────── #

@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig: Any) -> Dict:
    """
    Passes HEADLESS and SLOWMO from .env into every browser launch.

    Priority for headless:
      1. pytest --headed flag  → always headed
      2. HEADLESS=false in .env → headed
      3. HEADLESS=true (default) → headless

    Priority for slow_mo:
      1. pytest --slowmo <ms> CLI flag → uses that value
      2. SLOWMO=<ms> in .env → uses that value
      3. default → 0 (no delay)
    """
    launch_args: Dict = {}

    # ── Headless ──────────────────────────────────────────────────────────── #
    cli_headed: bool = pytestconfig.getoption("--headed", default=False)
    launch_args["headless"] = False if cli_headed else config.HEADLESS

    # ── Slow-motion ───────────────────────────────────────────────────────── #
    # CLI --slowmo takes priority; fall back to SLOWMO in .env
    cli_slowmo: int = pytestconfig.getoption("--slowmo", default=0)
    slowmo: int = cli_slowmo if cli_slowmo else config.SLOWMO
    if slowmo:
        launch_args["slow_mo"] = slowmo

    return launch_args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict) -> Dict:
    """Inject viewport dimensions from config into every browser context."""
    return {
        **browser_context_args,
        "viewport": {
            "width":  config.VIEWPORT_WIDTH,
            "height": config.VIEWPORT_HEIGHT,
        },
    }


# ──────────────────────────────────────────────────────────────────────────── #
#  Page-Object fixtures                                                        #
# ──────────────────────────────────────────────────────────────────────────── #

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage bound to the current Playwright page."""
    return LoginPage(page, config.BASE_URL)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """InventoryPage bound to the current Playwright page."""
    return InventoryPage(page)


# ──────────────────────────────────────────────────────────────────────────── #
#  Data fixtures                                                               #
# ──────────────────────────────────────────────────────────────────────────── #

_fake = Faker()


@pytest.fixture
def fake_user() -> dict:
    """Returns randomly generated (invalid) user data via Faker."""
    return {
        "first_name": _fake.first_name(),
        "last_name":  _fake.last_name(),
        "email":      _fake.email(),
        "username":   _fake.user_name(),
        "password":   _fake.password(length=12, special_chars=True),
        "address":    _fake.address(),
        "phone":      _fake.phone_number(),
    }


@pytest.fixture
def valid_creds() -> dict:
    """Real SauceDemo credentials sourced from config / .env."""
    return {
        "username": config.USERNAME,
        "password": config.PASSWORD,
    }


@pytest.fixture
def invalid_creds(fake_user: dict) -> dict:
    """Faker-based credentials guaranteed to fail SauceDemo login."""
    return {
        "username": fake_user["username"],
        "password": fake_user["password"],
    }