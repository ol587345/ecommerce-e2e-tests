from playwright.sync_api import expect

from pages.automation_exercise.products_page import ProductsPage


def test_search_products(page):
    products = ProductsPage(page).open()
    products.search("Jeans")

    expect(products.heading).to_have_text("Searched Products")
    names = products.names()
    assert names, "Search returned no products"
    assert all("jeans" in n.lower() for n in names), names


def test_filter_by_category(page):
    products = ProductsPage(page).open()
    products.filter_by_category("Women", "Dress")

    expect(products.heading).to_have_text("Women - Dress Products")
    assert products.names(), "Category page shows no products"


def test_filter_by_brand_matches_sidebar_count(page):
    products = ProductsPage(page).open()
    expected_count = products.brand_count_in_sidebar("Polo")

    products.filter_by_brand("Polo")

    expect(products.heading).to_have_text("Brand - Polo Products")
    expect(products.product_names).to_have_count(expected_count)
