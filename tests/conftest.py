"""conftest.py – shared fixtures for the SauceDemo POM test suite.

Features
--------
- HEADLESS + SLOWMO wired from .env into Playwright launch args
- Playwright traces recorded on every test; kept only on failure
- Screenshots captured automatically on test failure
- Page context configured with viewport from config
"""

import os
from pathlib import Path
from typing import Any, Dict, Generator

import pytest
from faker import Faker
from playwright.sync_api import Page, BrowserContext

from config import config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# ── Output directories ────────────────────────────────────────────────────── #
REPORTS_DIR    = Path("reports")
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
TRACES_DIR      = REPORTS_DIR / "traces"

for _d in (SCREENSHOTS_DIR, TRACES_DIR):
    _d.mkdir(parents=True, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────────── #
#  Browser launch args: HEADLESS + SLOWMO from .env                            #
# ──────────────────────────────────────────────────────────────────────────── #

@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig: Any) -> Dict:
    """
    Passes HEADLESS and SLOWMO from .env into every browser launch.

    Priority – headless:
      1. pytest --headed flag  → always headed
      2. HEADLESS=false in .env → headed
      3. HEADLESS=true (default) → headless

    Priority – slow_mo:
      1. pytest --slowmo <ms> flag
      2. SLOWMO=<ms> in .env
      3. default → 0
    """
    launch_args: Dict = {}

    cli_headed: bool = pytestconfig.getoption("--headed", default=False)
    launch_args["headless"] = False if cli_headed else config.HEADLESS

    cli_slowmo: int = pytestconfig.getoption("--slowmo", default=0)
    slowmo: int = cli_slowmo if cli_slowmo else config.SLOWMO
    if slowmo:
        launch_args["slow_mo"] = slowmo

    return launch_args


# ──────────────────────────────────────────────────────────────────────────── #
#  Browser context: viewport + tracing                                         #
# ──────────────────────────────────────────────────────────────────────────── #

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict) -> Dict:
    """Viewport + enable trace/screenshot/screencast collection."""
    return {
        **browser_context_args,
        "viewport": {
            "width":  config.VIEWPORT_WIDTH,
            "height": config.VIEWPORT_HEIGHT,
        },
        # Enables Playwright to record traces when we call start/stop
        "record_video_dir": None,   # video off by default; flip to str path to enable
    }


@pytest.fixture(autouse=True)
def manage_trace_and_screenshot(
    context: BrowserContext,
    page: Page,
    request: pytest.FixtureRequest,
) -> Generator[None, None, None]:
    """
    Per-test fixture (autouse) that:
      1. Starts a Playwright trace before each test.
      2. On FAILURE  → saves the trace zip + a full-page screenshot.
      3. On PASS     → discards the trace (keeps artifact folder clean).
    """
    # Sanitise test name for use as a filename
    safe_name = request.node.nodeid.replace("/", "_").replace("::", "__").replace(" ", "_")

    # ── Start trace ───────────────────────────────────────────────── #
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield   # test runs here

    # ── After test ────────────────────────────────────────────────── #
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False

    if failed:
        # Screenshot
        screenshot_path = SCREENSHOTS_DIR / f"{safe_name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        # Trace zip
        trace_path = TRACES_DIR / f"{safe_name}.zip"
        context.tracing.stop(path=str(trace_path))

        print(f"\n  📸 Screenshot : {screenshot_path}")
        print(f"  🔍 Trace      : {trace_path}")
        print(f"     View trace : npx playwright show-trace {trace_path}")
    else:
        # Discard trace — no cost, keeps folder tidy
        context.tracing.stop()


# ── Hook to expose test result inside fixtures ────────────────────────────── #
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ──────────────────────────────────────────────────────────────────────────── #
#  Page-Object fixtures                                                        #
# ──────────────────────────────────────────────────────────────────────────── #

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page, config.BASE_URL)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


# ──────────────────────────────────────────────────────────────────────────── #
#  Data fixtures                                                               #
# ──────────────────────────────────────────────────────────────────────────── #

_fake = Faker()


@pytest.fixture
def fake_user() -> dict:
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
    return {"username": config.USERNAME, "password": config.PASSWORD}


@pytest.fixture
def invalid_creds(fake_user: dict) -> dict:
    return {"username": fake_user["username"], "password": fake_user["password"]}