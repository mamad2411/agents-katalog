---
name: WebApp Testing with Playwright
description: Anthropic's official web application testing skill using native Python Playwright scripts with helper utilities for server lifecycle management, browser automation, and comprehensive E2E testing workflows.
version: 1.0.0
author: thetestingacademy
license: MIT
tags: [playwright-python, webapp-testing, e2e, anthropic, server-lifecycle, browser-automation, python]
testingTypes: [e2e, integration, functional]
frameworks: [playwright]
languages: [python]
domains: [web]
agents: [claude-code, cursor, github-copilot, windsurf, codex, aider, continue, cline, zed, bolt]
---

# WebApp Testing with Playwright (Python)

You are an expert QA automation engineer using Anthropic's official webapp-testing skill. This skill specializes in Python-based Playwright testing with integrated server lifecycle management. When the user asks you to test web applications, write E2E tests, or manage test environments, follow these detailed instructions.

## Core Principles

1. **Server lifecycle integration** -- Automatically start/stop application servers for isolated test runs.
2. **Python-native Playwright** -- Leverage Python's ecosystem with Playwright's browser automation.
3. **Helper script utilities** -- Use provided helper scripts for common test setup tasks.
4. **Isolated test environments** -- Each test run gets a clean server instance.
5. **Comprehensive assertions** -- Validate both UI state and underlying data consistency.

## Installation

```bash
# Install Playwright for Python
pip install playwright pytest-playwright

# Install Playwright browsers
playwright install

# Install with additional dependencies
pip install playwright pytest-playwright pytest-asyncio faker
```

## Project Structure

```
tests/
  webapp/
    test_authentication.py
    test_dashboard.py
    test_checkout.py
    test_api_integration.py
  fixtures/
    server_fixture.py
    browser_fixture.py
    data_fixture.py
  helpers/
    server_manager.py
    browser_utils.py
    test_data.py
  pages/
    login_page.py
    dashboard_page.py
    base_page.py
  config/
    test_config.py
    server_config.py
pytest.ini
conftest.py
```

## Server Lifecycle Management

### Server Manager Helper

```python
# helpers/server_manager.py
import subprocess
import time
import requests
from typing import Optional
import signal
import sys

class ServerManager:
    """Manage application server lifecycle for testing."""

    def __init__(
        self,
        command: str,
        port: int = 3000,
        host: str = "localhost",
        startup_timeout: int = 30,
        health_check_path: str = "/",
    ):
        self.command = command
        self.port = port
        self.host = host
        self.startup_timeout = startup_timeout
        self.health_check_path = health_check_path
        self.process: Optional[subprocess.Popen] = None
        self.base_url = f"http://{host}:{port}"

    def start(self) -> None:
        """Start the application server."""
        print(f"Starting server: {self.command}")

        self.process = subprocess.Popen(
            self.command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN)
        )

        # Wait for server to be ready
        self._wait_for_server()
        print(f"Server running at {self.base_url}")

    def _wait_for_server(self) -> None:
        """Wait for server to respond to health checks."""
        start_time = time.time()
        health_url = f"{self.base_url}{self.health_check_path}"

        while time.time() - start_time < self.startup_timeout:
            try:
                response = requests.get(health_url, timeout=1)
                if response.status_code < 500:
                    print(f"Server ready (status: {response.status_code})")
                    return
            except requests.exceptions.RequestException:
                pass

            time.sleep(0.5)

        raise TimeoutError(
            f"Server did not start within {self.startup_timeout} seconds"
        )

    def stop(self) -> None:
        """Stop the application server."""
        if self.process:
            print("Stopping server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("Server did not stop gracefully, forcing...")
                self.process.kill()
                self.process.wait()

            self.process = None
            print("Server stopped")

    def restart(self) -> None:
        """Restart the server."""
        self.stop()
        time.sleep(1)
        self.start()

    def is_running(self) -> bool:
        """Check if server is running."""
        if not self.process:
            return False

        try:
            response = requests.get(
                f"{self.base_url}{self.health_check_path}",
                timeout=1
            )
            return response.status_code < 500
        except requests.exceptions.RequestException:
            return False

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
```

### Server Fixture Configuration

```python
# conftest.py
import pytest
from helpers.server_manager import ServerManager

@pytest.fixture(scope="session")
def server():
    """Start application server for test session."""
    server_manager = ServerManager(
        command="npm run dev",
        port=3000,
        startup_timeout=60,
        health_check_path="/api/health"
    )

    server_manager.start()
    yield server_manager
    server_manager.stop()

@pytest.fixture(scope="session")
def base_url(server):
    """Provide base URL for tests."""
    return server.base_url

@pytest.fixture(scope="function")
def page(browser, base_url):
    """Create new page for each test."""
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    yield page
    context.close()
```

## Page Object Model (Python)

### Base Page Class

```python
# pages/base_page.py
from playwright.sync_api import Page, expect
from typing import Optional

class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = "") -> None:
        """Navigate to a specific path."""
        url = f"{self.base_url}{path}"
        self.page.goto(url)

    def wait_for_load(self, state: str = "networkidle") -> None:
        """Wait for page to load."""
        self.page.wait_for_load_state(state)

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def take_screenshot(self, filename: str, full_page: bool = True) -> None:
        """Take screenshot of page."""
        self.page.screenshot(path=filename, full_page=full_page)

    def wait_for_selector(
        self,
        selector: str,
        state: str = "visible",
        timeout: int = 30000
    ) -> None:
        """Wait for element to be in specific state."""
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

    def execute_script(self, script: str, *args):
        """Execute JavaScript in page context."""
        return self.page.evaluate(script, *args)

    def reload(self) -> None:
        """Reload the page."""
        self.page.reload()

    def go_back(self) -> None:
        """Navigate back."""
        self.page.go_back()

    def go_forward(self) -> None:
        """Navigate forward."""
        self.page.go_forward()
```

### Login Page Example

```python
# pages/login_page.py
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Login page object."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        # Locators
        self.email_input = page.get_by_label("Email")
        self.password_input = page.get_by_label("Password")
        self.submit_button = page.get_by_role("button", name="Sign in")
        self.error_message = page.get_by_role("alert")
        self.forgot_password_link = page.get_by_role("link", name="Forgot password?")
        self.remember_me_checkbox = page.get_by_label("Remember me")

    def goto(self) -> None:
        """Navigate to login page."""
        self.navigate("/login")

    def login(self, email: str, password: str, remember_me: bool = False) -> None:
        """Perform login action."""
        self.email_input.fill(email)
        self.password_input.fill(password)

        if remember_me:
            self.remember_me_checkbox.check()

        self.submit_button.click()

    def expect_error(self, message: str) -> None:
        """Verify error message is displayed."""
        expect(self.error_message).to_be_visible()
        expect(self.error_message).to_have_text(message)

    def expect_logged_in(self) -> None:
        """Verify successful login."""
        expect(self.page).to_have_url("/dashboard")

    def click_forgot_password(self) -> None:
        """Click forgot password link."""
        self.forgot_password_link.click()
        expect(self.page).to_have_url("/forgot-password")
```

### Dashboard Page Example

```python
# pages/dashboard_page.py
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from typing import List, Dict

class DashboardPage(BasePage):
    """Dashboard page object."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        # Locators
        self.welcome_heading = page.get_by_role("heading", name="Welcome")
        self.user_menu = page.get_by_test_id("user-menu")
        self.logout_button = page.get_by_role("button", name="Logout")
        self.stats_cards = page.locator(".stat-card")
        self.activity_feed = page.get_by_test_id("activity-feed")

    def goto(self) -> None:
        """Navigate to dashboard."""
        self.navigate("/dashboard")

    def expect_welcome_message(self, username: str) -> None:
        """Verify welcome message contains username."""
        expect(self.welcome_heading).to_contain_text(username)

    def get_stat_value(self, stat_name: str) -> str:
        """Get value for specific stat."""
        stat_card = self.page.locator(f".stat-card[data-stat='{stat_name}']")
        return stat_card.locator(".stat-value").text_content()

    def get_all_stats(self) -> Dict[str, str]:
        """Get all dashboard statistics."""
        stats = {}
        count = self.stats_cards.count()

        for i in range(count):
            card = self.stats_cards.nth(i)
            name = card.get_attribute("data-stat")
            value = card.locator(".stat-value").text_content()
            stats[name] = value

        return stats

    def logout(self) -> None:
        """Logout user."""
        self.user_menu.click()
        self.logout_button.click()
        expect(self.page).to_have_url("/login")

    def get_recent_activities(self, limit: int = 5) -> List[Dict[str, str]]:
        """Get recent activity items."""
        activities = []
        items = self.activity_feed.locator(".activity-item").all()[:limit]

        for item in items:
            activities.append({
                "title": item.locator(".activity-title").text_content(),
                "time": item.locator(".activity-time").text_content(),
                "type": item.get_attribute("data-type")
            })

        return activities
```

## Writing Tests

### Basic Test Structure

```python
# tests/webapp/test_authentication.py
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestAuthentication:
    """Authentication test suite."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Setup for each test."""
        self.login_page = LoginPage(page, base_url)
        self.dashboard_page = DashboardPage(page, base_url)

    def test_successful_login(self):
        """Test successful login with valid credentials."""
        self.login_page.goto()
        self.login_page.login("user@example.com", "SecurePass123!")

        self.login_page.expect_logged_in()
        self.dashboard_page.expect_welcome_message("User")

    def test_login_with_invalid_password(self):
        """Test login fails with incorrect password."""
        self.login_page.goto()
        self.login_page.login("user@example.com", "wrongpassword")

        self.login_page.expect_error("Invalid email or password")

    def test_login_with_nonexistent_email(self):
        """Test login fails with non-registered email."""
        self.login_page.goto()
        self.login_page.login("nonexistent@example.com", "SomePass123!")

        self.login_page.expect_error("Invalid email or password")

    @pytest.mark.parametrize("email,password,error", [
        ("", "password", "Email is required"),
        ("user@example.com", "", "Password is required"),
        ("invalid-email", "password", "Please enter a valid email"),
        ("user@example.com", "short", "Password must be at least 8 characters"),
    ])
    def test_login_validation(self, email: str, password: str, error: str):
        """Test form validation errors."""
        self.login_page.goto()
        self.login_page.email_input.fill(email)
        self.login_page.password_input.fill(password)
        self.login_page.submit_button.click()

        self.login_page.expect_error(error)

    def test_remember_me_functionality(self, page: Page):
        """Test remember me checkbox persists session."""
        self.login_page.goto()
        self.login_page.login("user@example.com", "SecurePass123!", remember_me=True)

        self.dashboard_page.expect_welcome_message("User")

        # Close and reopen browser
        page.context().close()
        new_context = page.context().browser.new_context()
        new_page = new_context.new_page()

        # Should still be logged in
        new_page.goto(f"{self.login_page.base_url}/dashboard")
        expect(new_page).to_have_url("/dashboard")

        new_context.close()
```

### Advanced Test Patterns

```python
# tests/webapp/test_dashboard.py
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class TestDashboard:
    """Dashboard functionality tests."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Setup authenticated session."""
        self.login_page = LoginPage(page, base_url)
        self.dashboard_page = DashboardPage(page, base_url)

        # Login before each test
        self.login_page.goto()
        self.login_page.login("user@example.com", "SecurePass123!")

    def test_dashboard_loads_all_components(self):
        """Test all dashboard components are visible."""
        self.dashboard_page.goto()

        expect(self.dashboard_page.welcome_heading).to_be_visible()
        expect(self.dashboard_page.stats_cards).to_have_count(4)
        expect(self.dashboard_page.activity_feed).to_be_visible()

    def test_dashboard_statistics_accuracy(self):
        """Test dashboard stats match expected values."""
        self.dashboard_page.goto()

        stats = self.dashboard_page.get_all_stats()

        assert "users" in stats
        assert "revenue" in stats
        assert "orders" in stats
        assert "growth" in stats

        # Verify stat values are numeric
        assert stats["users"].isdigit()
        assert "$" in stats["revenue"]

    def test_activity_feed_updates(self, page: Page):
        """Test activity feed shows recent actions."""
        self.dashboard_page.goto()

        initial_activities = self.dashboard_page.get_recent_activities()
        initial_count = len(initial_activities)

        # Perform an action that generates activity
        page.get_by_role("button", name="Create New").click()
        page.get_by_label("Title").fill("Test Item")
        page.get_by_role("button", name="Save").click()

        # Wait for activity feed to update
        page.wait_for_timeout(1000)
        self.dashboard_page.reload()

        updated_activities = self.dashboard_page.get_recent_activities()

        assert len(updated_activities) > initial_count
        assert updated_activities[0]["title"] == "Created Test Item"

    def test_logout_functionality(self):
        """Test user can logout successfully."""
        self.dashboard_page.goto()
        self.dashboard_page.logout()

        expect(self.login_page.page).to_have_url("/login")

        # Verify cannot access dashboard after logout
        self.dashboard_page.goto()
        expect(self.login_page.page).to_have_url("/login")
```

## Test Data Management

### Test Data Helper

```python
# helpers/test_data.py
from faker import Faker
from typing import Dict, List
import random

fake = Faker()

class TestDataGenerator:
    """Generate realistic test data."""

    @staticmethod
    def user(
        email: str = None,
        password: str = "SecurePass123!",
        **kwargs
    ) -> Dict[str, str]:
        """Generate user data."""
        return {
            "email": email or fake.email(),
            "password": password,
            "firstName": kwargs.get("firstName", fake.first_name()),
            "lastName": kwargs.get("lastName", fake.last_name()),
            "phone": kwargs.get("phone", fake.phone_number()),
            "address": kwargs.get("address", fake.address()),
        }

    @staticmethod
    def product(**kwargs) -> Dict:
        """Generate product data."""
        return {
            "name": kwargs.get("name", fake.catch_phrase()),
            "description": kwargs.get("description", fake.text(max_nb_chars=200)),
            "price": kwargs.get("price", round(random.uniform(10, 1000), 2)),
            "category": kwargs.get("category", random.choice(["Electronics", "Clothing", "Books", "Home"])),
            "stock": kwargs.get("stock", random.randint(0, 100)),
        }

    @staticmethod
    def order(user_id: str, products: List[Dict]) -> Dict:
        """Generate order data."""
        return {
            "userId": user_id,
            "products": products,
            "total": sum(p["price"] * p["quantity"] for p in products),
            "status": random.choice(["pending", "processing", "shipped", "delivered"]),
            "createdAt": fake.date_time_this_month().isoformat(),
        }
```

### Using Test Data in Tests

```python
# tests/webapp/test_checkout.py
import pytest
from helpers.test_data import TestDataGenerator

class TestCheckout:
    """Checkout flow tests."""

    @pytest.fixture
    def test_user(self):
        """Generate test user."""
        return TestDataGenerator.user()

    @pytest.fixture
    def test_products(self):
        """Generate test products."""
        return [
            TestDataGenerator.product(name="Widget A", price=29.99),
            TestDataGenerator.product(name="Widget B", price=49.99),
        ]

    def test_checkout_flow(self, page, base_url, test_user, test_products):
        """Test complete checkout flow."""
        # Navigate and login
        page.goto(f"{base_url}/login")
        page.get_by_label("Email").fill(test_user["email"])
        page.get_by_label("Password").fill(test_user["password"])
        page.get_by_role("button", name="Sign in").click()

        # Add products to cart
        for product in test_products:
            page.goto(f"{base_url}/products")
            page.get_by_text(product["name"]).click()
            page.get_by_role("button", name="Add to Cart").click()

        # Proceed to checkout
        page.get_by_test_id("cart-icon").click()
        expect(page.get_by_test_id("cart-items")).to_have_count(len(test_products))

        page.get_by_role("button", name="Checkout").click()

        # Fill shipping information
        page.get_by_label("Name").fill(f"{test_user['firstName']} {test_user['lastName']}")
        page.get_by_label("Address").fill(test_user["address"])
        page.get_by_label("Phone").fill(test_user["phone"])

        # Complete order
        page.get_by_role("button", name="Place Order").click()

        # Verify success
        expect(page.get_by_text("Order confirmed")).to_be_visible()
        expect(page).to_have_url("/orders/confirmation")
```

## Server Lifecycle Patterns

### Multiple Server Configurations

```python
# conftest.py
import pytest
from helpers.server_manager import ServerManager

@pytest.fixture(scope="session", params=["development", "production"])
def server(request):
    """Run tests against different server configurations."""
    config = {
        "development": {
            "command": "npm run dev",
            "port": 3000,
        },
        "production": {
            "command": "npm run build && npm start",
            "port": 8080,
        }
    }

    cfg = config[request.param]
    server_manager = ServerManager(
        command=cfg["command"],
        port=cfg["port"]
    )

    server_manager.start()
    yield server_manager
    server_manager.stop()
```

### Database Seeding Integration

```python
# helpers/server_manager.py (extended)
class ServerManager:
    # ... previous methods ...

    def seed_database(self, seed_script: str) -> None:
        """Run database seed script."""
        print("Seeding database...")
        result = subprocess.run(
            seed_script,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Database seeding failed: {result.stderr}")

        print("Database seeded successfully")

    def reset_database(self, reset_script: str) -> None:
        """Reset database to clean state."""
        print("Resetting database...")
        subprocess.run(reset_script, shell=True, check=True)
        print("Database reset complete")

# conftest.py
@pytest.fixture(scope="function")
def clean_database(server):
    """Provide clean database for each test."""
    server.reset_database("npm run db:reset")
    server.seed_database("npm run db:seed")
    yield
```

## Best Practices

1. **Use server fixtures** to ensure clean test environment for each run.
2. **Implement Page Object Model** to separate test logic from page structure.
3. **Generate test data dynamically** using Faker for realistic scenarios.
4. **Take screenshots on failure** to aid debugging.
5. **Use descriptive test names** that explain what is being tested.
6. **Isolate test data** to prevent test interdependencies.
7. **Verify server health** before running tests.
8. **Clean up resources** in fixtures to prevent leaks.
9. **Use parametrize** for testing multiple scenarios efficiently.
10. **Document helper functions** for team knowledge sharing.

## Anti-Patterns to Avoid

1. **Not stopping servers** -- Always clean up in fixtures.
2. **Hardcoded URLs** -- Use base_url fixture.
3. **Shared test state** -- Each test should be independent.
4. **Ignoring server startup failures** -- Implement proper health checks.
5. **Not waiting for elements** -- Use Playwright's auto-waiting assertions.
6. **Overly complex page objects** -- Keep methods focused and simple.
7. **Skipping cleanup** -- Always reset database between tests.
8. **Testing implementation details** -- Focus on user-facing behavior.
9. **No error handling in helpers** -- Implement proper exception handling.
10. **Ignoring test execution time** -- Optimize slow tests for CI/CD.

This skill provides a comprehensive foundation for Python-based web application testing with Playwright, featuring integrated server lifecycle management and helper utilities optimized for Anthropic's testing workflows.
