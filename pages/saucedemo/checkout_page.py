import re

from playwright.sync_api import Page


class CheckoutPage:
    """Covers all three checkout steps: your information, overview, complete."""

    def __init__(self, page: Page):
        self.page = page
        # Step 1 - your information
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.error = page.locator('[data-test="error"]')
        # Step 2 - overview
        self.item_total = page.locator('[data-test="subtotal-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        # Step 3 - complete
        self.complete_header = page.locator('[data-test="complete-header"]')

    def fill_information(self, first: str, last: str, postal: str) -> None:
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()

    def item_total_value(self) -> float:
        """'Item total: $39.98' -> 39.98"""
        return float(re.search(r"\$([\d.]+)", self.item_total.inner_text()).group(1))

    def finish(self) -> None:
        self.finish_button.click()
