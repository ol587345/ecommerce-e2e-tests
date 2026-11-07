from playwright.sync_api import Page

from framework.config import AE_BASE_URL


class AELoginPage:
    """The /login page holds both the 'Login' form and the 'New User Signup' form."""

    def __init__(self, page: Page):
        self.page = page
        self.email = page.locator('[data-qa="login-email"]')
        self.password = page.locator('[data-qa="login-password"]')
        self.login_button = page.locator('[data-qa="login-button"]')
        self.error = page.get_by_text("Your email or password is incorrect!")
        self.logged_in_as = page.locator("a", has_text="Logged in as")

    def open(self) -> "AELoginPage":
        self.page.goto(f"{AE_BASE_URL}/login")
        return self

    def login(self, email: str, password: str) -> None:
        self.email.fill(email)
        self.password.fill(password)
        self.login_button.click()

    def email_validation_message(self) -> str:
        """The browser's built-in (HTML5) validation text for the email field, e.g. 'Please fill out this field.'"""
        return self.email.evaluate("el => el.validationMessage")
