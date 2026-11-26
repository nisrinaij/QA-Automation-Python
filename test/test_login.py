from playwright.sync_api import Page, expect

from pages.login import LoginPage
from config import DASHBOARD_URL, VALID_USERNAME, VALID_PASSWORD

# TC-login-01: Valid login
def test_valid_login(login_page):

    login = LoginPage(login_page)
 
    login.goto()
    login_page.wait_for_load_state("networkidle")

    login.fill_username(VALID_USERNAME)
    login.fill_password(VALID_PASSWORD)
    login.click_login()

    expect(login_page).to_have_url(DASHBOARD_URL)

# TC-login-02: Invalid login
def test_invalid_login(login_page):

    login = LoginPage(login_page)

    login.goto()
    login_page.wait_for_load_state("networkidle")

    login.fill_username("unknown_user")
    login.fill_password(VALID_PASSWORD)
    login.click_login()

    expect(login_page.get_by_text("Invalid credentials")).to_be_visible()

