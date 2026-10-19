
import os
from playwright.sync_api import sync_playwright

import config

LOGIN_URL = config.LOGIN_URL
AUTH_FILE = config.AUTH_FILE


def generate_storage_state():

    with sync_playwright() as p:
        p.selectors.set_test_id_attribute("data-test")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # open login page
        page.goto(LOGIN_URL)

        # login
        page.get_by_placeholder("Username").fill(config.VALID_USERNAME)
        page.get_by_placeholder("Password").fill(config.VALID_PASSWORD)
        page.get_by_role("button", name="Login").click()

        context.storage_state(path=AUTH_FILE)
        print(f"authentication state saved to {AUTH_FILE}")

        # Cleanup
        page.close()
        context.close()
        browser.close()


if __name__ == "__main__":
    generate_storage_state()