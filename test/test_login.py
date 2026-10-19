from playwright.sync_api import Page, expect

from pages.login import LoginPage
from config import BASE_URL, VALID_USERNAME, VALID_PASSWORD


def test_valid_login(page: Page):

    login = LoginPage(page)

    login.goto()

    login.fill_username(VALID_USERNAME)
    login.fill_password(VALID_PASSWORD)
    login.click_login()

    expect(page).to_have_url(BASE_URL)

def test_invalid_login(page: Page):

    login = LoginPage(page)

    login.goto()

    login.fill_username("unknown_user")
    login.fill_password(VALID_PASSWORD)
    login.click_login()

    expect(page.get_by_text("Invalid credentials")).to_be_visible()


#  page.get_by_role("link", name="Admin").click()
#     page.get_by_role("button", name=" Add").click()
#     page.get_by_role("textbox", name="Type for hints...").click()
#     page.get_by_role("textbox", name="Type for hints...").fill("user7")
#     page.get_by_text("-- Select --").first.click()
#     page.get_by_role("textbox", name="Type for hints...").click()
#     page.get_by_role("textbox", name="Type for hints...").fill("")
#     page.get_by_role("link", name="Directory").click()
#     page.get_by_role("link", name="PIM").click()
#     page.get_by_role("link", name="Add Employee").click()
#     page.get_by_role("link", name="Employee List").click()
#     page.get_by_role("button", name=" Add").click()
#     page.get_by_role("textbox", name="First Name").click()
#     page.get_by_role("textbox", name="First Name").fill("user")
#     page.get_by_role("textbox", name="Middle Name").click()
#     page.get_by_role("textbox", name="Last Name").click()
#     page.get_by_role("textbox", name="Last Name").fill("77")
#     page.get_by_role("textbox").nth(4).click()
#     page.get_by_role("textbox").nth(4).fill("0499")
#     page.locator(".oxd-switch-input").click()
#     page.locator(".oxd-switch-input").click()
#     page.get_by_role("button", name="Save").click()
#     page.get_by_role("link", name="Employee List").click()
#     page.get_by_role("textbox", name="Type for hints...").first.click()
#     page.get_by_role("textbox", name="Type for hints...").first.fill("user77")
#     page.get_by_role("button", name="Search").click()
#     page.get_by_role("link", name="Admin").click()
#     page.get_by_role("link", name="PIM").click()
#     page.get_by_role("textbox", name="Type for hints...").first.click()
#     page.get_by_role("textbox", name="Type for hints...").first.fill("user77")
#     page.get_by_role("button", name="Search").click()
#     page.get_by_role("textbox", name="Type for hints...").first.click()
#     page.get_by_role("textbox", name="Type for hints...").first.fill("")
#     page.get_by_role("textbox").nth(2).click()
#     page.get_by_role("textbox").nth(2).fill("0499")
#     page.get_by_role("button", name="Search").click()
#     expect(page.get_by_role("cell", name="0499")).to_be_visible()
