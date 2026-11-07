import pytest
from playwright.sync_api import expect

from pages.saucedemo.cart_page import CartPage
from pages.saucedemo.checkout_page import CheckoutPage

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt"]


def test_full_checkout_flow(sauce_inventory, page, screenshot):
    expected_total = sum(sauce_inventory.price_of(p) for p in PRODUCTS)
    for product in PRODUCTS:
        sauce_inventory.add_to_cart(product)
    screenshot("products added")
    sauce_inventory.go_to_cart()
    screenshot("cart")
    CartPage(page).checkout()

    checkout = CheckoutPage(page)
    checkout.fill_information("Olga", "Tester", "12345")
    screenshot("checkout overview")
    assert checkout.item_total_value() == pytest.approx(expected_total)

    checkout.finish()
    expect(checkout.complete_header).to_have_text("Thank you for your order!")


@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Tester", "12345", "First Name is required"),
        ("Olga", "", "12345", "Last Name is required"),
        ("Olga", "Tester", "", "Postal Code is required"),
    ],
    ids=["missing-first-name", "missing-last-name", "missing-postal-code"],
)
def test_checkout_form_validation(sauce_inventory, page, screenshot, first, last, postal, expected_error):
    sauce_inventory.add_to_cart(PRODUCTS[0])
    sauce_inventory.go_to_cart()
    screenshot("cart")
    CartPage(page).checkout()

    checkout = CheckoutPage(page)
    checkout.fill_information(first, last, postal)

    expect(checkout.error).to_contain_text(expected_error)
