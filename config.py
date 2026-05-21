"""config.py – reads runtime settings from environment variables (or a .env file).

Priority: real env vars > .env file values > defaults below.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project root (silently ignored if absent)
_env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_env_path, override=False)


def _bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    # SauceDemo target
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")

    # Default credentials (standard_user works out-of-the-box)
    USERNAME: str = os.getenv("USERNAME", "standard_user")
    PASSWORD: str = os.getenv("PASSWORD", "secret_sauce")

    # Browser / execution
    BROWSER: str = os.getenv("BROWSER", "chromium")  # chromium | firefox | webkit
    HEADLESS: bool = _bool(os.getenv("HEADLESS", "true"))

    # Slow-motion delay between every Playwright action (ms)
    # 0 = off  |  500 = comfortable  |  1000 = slow  |  2000 = very slow
    SLOWMO: int = int(os.getenv("SLOWMO", "0"))

    # Playwright viewport
    VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1280"))
    VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "720"))

    # Timeouts (ms)
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
    NAVIGATION_TIMEOUT: int = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))

    # Reports
    HTML_REPORT: str = os.getenv("HTML_REPORT", "reports/report.html")


config = Config()