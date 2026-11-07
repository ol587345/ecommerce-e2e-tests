from playwright.sync_api import Page


def slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (how Sauce Demo builds its data-test ids)."""
    return product_name.lower().replace(" ", "-")


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_prices = page.locator('[data-test="inventory-item-price"]')
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')

    def add_to_cart(self, product_name: str) -> None:
        self.page.locator(f'[data-test="add-to-cart-{slug(product_name)}"]').click()

    def remove_from_cart(self, product_name: str) -> None:
        self.page.locator(f'[data-test="remove-{slug(product_name)}"]').click()

    def sort_by(self, option_value: str) -> None:
        """option_value: 'az', 'za', 'lohi' or 'hilo'."""
        self.sort_dropdown.select_option(option_value)

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.item_prices.all_inner_texts()]

    def price_of(self, product_name: str) -> float:
        item = self.page.locator('[data-test="inventory-item"]').filter(has_text=product_name)
        return float(item.locator('[data-test="inventory-item-price"]').inner_text().replace("$", ""))

    def go_to_cart(self) -> None:
        self.cart_link.click()
        # Wait for navigation, otherwise the next read can still see the inventory page.
        self.page.wait_for_url("**/cart.html")
