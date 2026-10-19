from playwright.sync_api import Page
from config import LOGIN_URL

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto(LOGIN_URL)

    def fill_username(self, username: str):
        self.page.get_by_placeholder("Username").fill(username)

    def fill_password(self, password: str):
        self.page.get_by_placeholder("Password").fill(password)

    def click_login(self):
        self.page.get_by_role("button", name="Login").click()