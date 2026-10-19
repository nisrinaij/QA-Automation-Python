# conftest.py
import os
import pytest
from playwright.sync_api import sync_playwright
import config 


@pytest.fixture
def login_page():
    """
    Fresh website page to test login features.
    """
    with sync_playwright() as p:
        p.selectors.set_test_id_attribute("data-test")
        browser = p.chromium.launch(headless=False)

        context = browser.new_context()
        page = context.new_page()

        yield page

        # Teardown
        page.close()
        context.close()
        browser.close()


@pytest.fixture
def page():
    """
    Logged-in page to test features that require authentication.
    """
    if not os.path.exists(config.AUTH_FILE):
        pytest.fail(
            f"File '{config.AUTH_FILE}' not found."
        )

    with sync_playwright() as p:
        p.selectors.set_test_id_attribute("data-test")
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(storage_state=config.AUTH_FILE)
        page = context.new_page()

        yield page

        # Teardown
        page.close()
        context.close()
        browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook used to capture a screenshot when a test fails.

    The hook executes for each test phase:
        setup → call → teardown

    We capture a screenshot only when the actual test execution
    phase fails.
    """

    outcome = yield
    report = outcome.get_result()

    # Capture screenshot only when the test itself fails.
    if report.when == "call" and report.failed:

        page = item.funcargs.get("page")

        if page:

            screenshot_dir = "reports/screenshots"

            os.makedirs(
                screenshot_dir,
                exist_ok=True
            )

            screenshot_path = os.path.join(
                screenshot_dir,
                f"{item.name}.png"
            )

            page.screenshot(
                path=screenshot_path,
                full_page=True
            )