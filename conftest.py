import os
import pytest
import config
import re

import threading
import time
import psutil

from pathlib import Path
from config import BASE_URL, LOGIN_URL, AUTH_FILE, DASHBOARD_URL


def pytest_configure(config):
    """
    Automatically configure HTML reporting based on the test execution.

    Full suite:
        reports/full_suite_test.html

    Individual test file:
        reports/<test_file>/<test_file>.html
    """

    # Check whether pytest-html is installed.
    if not config.pluginmanager.hasplugin("html"):
        return

    # Respect a manually specified --html argument.
    if config.option.htmlpath:
        return

    # Identify Python test files passed through the CLI.
    test_files = []

    for arg in config.args:
        # Remove test node identifiers, if present.
        test_path = arg.split("::")[0]
        path = Path(test_path)

        if path.suffix == ".py" and path.exists():
            test_files.append(path)

    # Determine report location.
    if len(test_files) == 1:
        test_name = test_files[0].stem

        report_dir = Path("reports") / test_name
        report_name = f"{test_name}.html"

    else:
        report_dir = Path("reports")
        report_name = "full_suite_test.html"

    # Create report directory.
    report_dir.mkdir(parents=True, exist_ok=True)

    # Configure pytest-html.
    config.option.htmlpath = str(report_dir / report_name)

    # Keep screenshots as external files.
    config.option.self_contained_html = False

@pytest.fixture
def login_page(playwright, browser):
    """
    Fresh website page to test login features.
    """
    # Set custom test ID attribute using the native playwright fixture
    playwright.selectors.set_test_id_attribute("data-test")
    
    context = browser.new_context()
    page = context.new_page()
    
    yield page
    
    context.close()

@pytest.fixture
def page(playwright, browser):
    """
    Logged-in page to test features that require authentication.
    """
    if not os.path.exists(config.AUTH_FILE):
        pytest.fail(f"File '{config.AUTH_FILE}' not found.")

    playwright.selectors.set_test_id_attribute("data-test")
    
    # Load the saved login session
    context = browser.new_context(storage_state=config.AUTH_FILE)
    page = context.new_page()
    
    # Tell the browser to go to the target page before handing it to the test
    page.goto(config.DASHBOARD_URL) 
    
    yield page
    
    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshots when a test fails and attach them
    to the corresponding pytest-html report.
    """

    outcome = yield
    report = outcome.get_result()

    # Only capture screenshots for test execution failures.
    if report.when != "call" or not report.failed:
        return

    # Check for available Playwright page fixtures.
    page = item.funcargs.get("page")

    if page is None:
        page = item.funcargs.get("login_page")

    if page is None:
        return

    # Get the configured HTML report location.
    html_report_path = item.config.option.htmlpath

    if not html_report_path:
        return

    # Determine screenshot directory.
    report_dir = Path(html_report_path).parent
    screenshot_dir = report_dir / "screenshots"

    screenshot_dir.mkdir(parents=True, exist_ok=True)

    # Generate a safe screenshot filename.
    safe_test_name = re.sub(
        r"[^a-zA-Z0-9_.-]",
        "_",
        item.nodeid
    )

    screenshot_filename = f"{safe_test_name}.png"

    screenshot_path = screenshot_dir / screenshot_filename

    try:
        # Capture screenshot.
        page.screenshot(
            path=str(screenshot_path),
            full_page=True
        )

        # Attach screenshot to HTML report.
        pytest_html = item.config.pluginmanager.getplugin("html")

        if pytest_html is not None:
            extras = getattr(report, "extras", [])

            extras.append(
                pytest_html.extras.image(
                    f"screenshots/{screenshot_filename}"
                )
            )

            report.extras = extras

    except Exception as error:
        print(f"Failed to capture screenshot: {error}")


@pytest.fixture(scope="session", autouse=True)
def monitor_system_resources():
    """
    Background thread fixture to record average and peak CPU and RAM usage
    during pytest Playwright test execution on Ubuntu.
    """
    process = psutil.Process()
    cpu_samples = []
    ram_samples = []
    monitoring = True

    def sample_resources():
        while monitoring:
            # Sample system-wide or process CPU utilization (%)
            cpu_samples.append(psutil.cpu_percent(interval=None))
            # Sample process memory consumption (RSS in MB)
            ram_samples.append(process.memory_info().rss / (1024 * 1024))
            time.sleep(0.5)  # Sample every 500 ms

    # Start sampling thread
    monitor_thread = threading.Thread(target=sample_resources, daemon=True)
    monitor_thread.start()

    yield  # Hand control over to pytest test execution

    # Teardown: Stop sampling and display metrics
    monitoring = False
    monitor_thread.join(timeout=1.0)

    if cpu_samples and ram_samples:
        avg_cpu = sum(cpu_samples) / len(cpu_samples)
        peak_cpu = max(cpu_samples)
        avg_ram = sum(ram_samples) / len(ram_samples)
        peak_ram = max(ram_samples)

        print("\n" + "=" * 50)
        print("SYSTEM RESOURCE UTILIZATION REPORT")
        print("=" * 50)
        print(f"Average CPU Utilization : {avg_cpu:.2f} %")
        print(f"Peak CPU Utilization    : {peak_cpu:.2f} %")
        print(f"Average RAM Consumption  : {avg_ram:.2f} MB")
        print(f"Peak RAM Consumption     : {peak_ram:.2f} MB")
        print("=" * 50)