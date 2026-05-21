# SAUCE_LAB
Page Object Model framework for the SauceDemo app
# SauceDemo – Playwright POM Framework

A production-ready **Page Object Model** test framework for [SauceDemo](https://www.saucedemo.com), built with **Playwright + pytest**, environment-based config, Faker-driven test data, and a GitHub Actions CI/CD pipeline.

---

## 📁 Project Structure

```
saucedemo-pom/
├── pages/
│   ├── __init__.py
│   ├── base_page.py        # BasePage – shared browser helpers
│   ├── login_page.py       # LoginPage POM
│   └── inventory_page.py   # InventoryPage POM
├── tests/
│   ├── __init__.py
│   ├── test_login_success.py   # Flow 1 – successful login
│   ├── test_login_failure.py   # Flow 2 – invalid credentials
│   └── test_cart.py            # Flow 3 – add item & verify cart count
├── .github/
│   └── workflows/
│       └── ui-tests.yml    # CI/CD pipeline
├── reports/                # Generated at runtime (git-ignored)
├── conftest.py             # Fixtures: browser, page objects, Faker data
├── config.py               # Reads settings from environment / .env
├── pytest.ini              # Markers, log settings, default flags
├── requirements.txt        # Pinned dependencies
├── .env.example            # Template – copy to .env and fill in values
└── README.md
```

---

## ⚡ Quick Start

### 1 – Clone & create a virtual environment

```bash
git clone https://github.com/<your-org>/saucedemo-pom.git
cd saucedemo-pom

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 2 – Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3 – Install Playwright browsers

```bash
# Install Chromium and Firefox (used in CI matrix)
python -m playwright install chromium firefox --with-deps
```

### 4 – Configure environment

```bash
cp .env.example .env
# Edit .env with your preferred values (the defaults work out-of-the-box)
```

Key variables:

| Variable             | Default                         | Description                          |
|----------------------|---------------------------------|--------------------------------------|
| `BASE_URL`           | `https://www.saucedemo.com`     | Target application URL               |
| `USERNAME`           | `standard_user`                 | SauceDemo login username             |
| `PASSWORD`           | `secret_sauce`                  | SauceDemo login password             |
| `BROWSER`            | `chromium`                      | `chromium` \| `firefox` \| `webkit`  |
| `HEADLESS`           | `true`                          | `true` for CI, `false` for debugging |
| `DEFAULT_TIMEOUT`    | `10000`                         | Element wait timeout (ms)            |
| `NAVIGATION_TIMEOUT` | `30000`                         | Page navigation timeout (ms)         |

---

## 🧪 Running Tests

### All tests (both browsers – matches CI)

```bash
pytest
```

### Single browser

```bash
pytest --browser-name=chromium
pytest --browser-name=firefox
```

### Specific marker

```bash
pytest -m smoke              # critical-path tests only
pytest -m "login and smoke"  # login smoke tests
pytest -m regression         # full regression suite
```

### Single test file

```bash
pytest tests/test_cart.py -v
```

### Show test report in browser

```bash
# After a run, open the self-contained HTML report:
open reports/report.html          # macOS
xdg-open reports/report.html      # Linux
start reports/report.html         # Windows
```

---

## 🏗️ Framework Architecture

### Page Object Model

| Class           | Responsibility                                         |
|-----------------|--------------------------------------------------------|
| `BasePage`      | Wraps Playwright `Page`; provides `click`, `fill`, `get_text`, navigation helpers |
| `LoginPage`     | Login form interactions and error assertions           |
| `InventoryPage` | Product listing, add-to-cart, badge count, navigation  |

### Test Flows

| Test file               | Scenarios covered                                                          |
|-------------------------|----------------------------------------------------------------------------|
| `test_login_success.py` | ✅ Valid credentials → lands on inventory, title = "Products"              |
| `test_login_failure.py` | ❌ Random creds, empty username, empty password, locked-out account        |
| `test_cart.py`          | 🛒 Add 1 item (badge = 1), add 2 items (badge = 2), count persists on nav |

### Fixtures (`conftest.py`)

| Fixture          | Scope    | Description                                           |
|------------------|----------|-------------------------------------------------------|
| `browser_name`   | function | Parametrized: `["chromium", "firefox"]`               |
| `page`           | function | Fresh Playwright `Page`; tears down browser after each test |
| `login_page`     | function | `LoginPage` bound to current `page`                  |
| `inventory_page` | function | `InventoryPage` bound to current `page`               |
| `fake_user`      | function | Faker-generated user dict (name, email, password …)  |
| `valid_creds`    | function | Real creds from `config.py`                           |
| `invalid_creds`  | function | Faker-based creds guaranteed to fail                  |

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ui-tests.yml`) runs on every push or pull request to `main` / `develop`.

**Matrix:** Chromium × Firefox (both headless on `ubuntu-latest`)

**Steps:**
1. Checkout code
2. Set up Python 3.12 (with pip cache)
3. `pip install -r requirements.txt`
4. `playwright install <browser> --with-deps`
5. `pytest` with browser-specific HTML report
6. Upload `reports/report-<browser>.html` + `pytest.log` as artefacts (14-day retention)
7. Aggregate job ensures both browsers must pass

### Trigger manually

```
GitHub → Actions → "UI Tests – SauceDemo POM" → Run workflow
```

---

## 🛠️ Development Tips

```bash
# Run tests in headed mode for visual debugging
HEADLESS=false pytest --browser-name=chromium -k test_successful_login

# Increase timeout for slow networks
DEFAULT_TIMEOUT=20000 pytest

# Run only the smoke suite on Firefox
pytest -m smoke --browser-name=firefox -v
```

---

## 📦 Dependencies

| Package           | Purpose                        |
|-------------------|--------------------------------|
| `pytest`          | Test runner                    |
| `playwright`      | Browser automation             |
| `pytest-playwright` | Playwright–pytest integration |
| `pytest-html`     | Self-contained HTML reports    |
| `python-dotenv`   | `.env` file loading            |
| `Faker`           | Dynamic test-data generation   |

---

## 📄 License

MIT – see `LICENSE` for details.
