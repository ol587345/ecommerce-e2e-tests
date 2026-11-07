from playwright.sync_api import Page

from framework.config import AE_BASE_URL


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.heading = page.locator(".features_items h2.title")
        self.product_names = page.locator(".features_items .productinfo p")

    def open(self) -> "ProductsPage":
        self.page.goto(f"{AE_BASE_URL}/products")
        return self

    def search(self, term: str) -> None:
        self.search_input.fill(term)
        self.search_button.click()

    def filter_by_category(self, parent: str, child: str) -> None:
        """Sidebar accordion, e.g. parent='Women', child='Dress'."""
        self.page.locator(f'a[href="#{parent}"]').click()
        self.page.locator(f"#{parent}").get_by_role("link", name=child).click()

    def filter_by_brand(self, brand: str) -> None:
        self.page.locator(f'.brands-name a[href="/brand_products/{brand}"]').click()

    def brand_count_in_sidebar(self, brand: str) -> int:
        """The sidebar shows '(6)POLO' - return the 6."""
        text = self.page.locator(f'.brands-name a[href="/brand_products/{brand}"] span').inner_text()
        return int(text.strip("()"))

    def names(self) -> list[str]:
        return self.product_names.all_inner_texts()
