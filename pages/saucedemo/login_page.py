from playwright.sync_api import Page

from framework.config import SAUCE_BASE_URL


class SauceLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator('[data-test="username"]')
        self.password = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error = page.locator('[data-test="error"]')

    def open(self) -> "SauceLoginPage":
        self.page.goto(SAUCE_BASE_URL)
        return self

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
