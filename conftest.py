import os
import pytest
import config

import threading
import time
import psutil

from config import BASE_URL, LOGIN_URL, AUTH_FILE, DASHBOARD_URL

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
    Pytest hook used to capture a screenshot when a test fails.
    """
    # 1. Retrieve the HTML plugin
    pytest_html = item.config.pluginmanager.getplugin("html")
    
    outcome = yield
    report = outcome.get_result()
    
    # 2. Initialize the extras list for the HTML report
    extras = getattr(report, "extras", [])

    # Capture screenshot only when the test itself fails.
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            screenshot_filename = f"{item.name}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_filename)
            
            page.screenshot(path=screenshot_path, full_page=True)
            
            # 3. Attach the screenshot to the report using a relative path
            if pytest_html is not None:
                extras.append(pytest_html.extras.image(f"screenshots/{screenshot_filename}"))
                
    # 4. Save the extras back to the report object
    report.extras = extras

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