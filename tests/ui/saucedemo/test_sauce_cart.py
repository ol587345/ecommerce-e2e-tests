from playwright.sync_api import expect

from pages.saucedemo.cart_page import CartPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


def test_add_one_item_to_cart(sauce_inventory, page):
    sauce_inventory.add_to_cart(BACKPACK)

    expect(sauce_inventory.cart_badge).to_have_text("1")
    sauce_inventory.go_to_cart()
    assert CartPage(page).names() == [BACKPACK]


def test_remove_item_updates_cart(sauce_inventory, page):
    sauce_inventory.add_to_cart(BACKPACK)
    sauce_inventory.add_to_cart(BIKE_LIGHT)
    expect(sauce_inventory.cart_badge).to_have_text("2")

    sauce_inventory.remove_from_cart(BACKPACK)

    expect(sauce_inventory.cart_badge).to_have_text("1")
    sauce_inventory.go_to_cart()
    assert CartPage(page).names() == [BIKE_LIGHT]
