import re

import pytest
from playwright.sync_api import expect

from framework.config import SAUCE_LOCKED_USER, SAUCE_PASSWORD, SAUCE_STANDARD_USER
from pages.saucedemo.inventory_page import InventoryPage
from pages.saucedemo.login_page import SauceLoginPage


def test_valid_login_opens_products_page(page):
    SauceLoginPage(page).open().login(SAUCE_STANDARD_USER, SAUCE_PASSWORD)

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(InventoryPage(page).title).to_have_text("Products")


@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        (SAUCE_STANDARD_USER, "wrong_password", "Username and password do not match any user in this service"),
        ("no_such_user", SAUCE_PASSWORD, "Username and password do not match any user in this service"),
        ("", SAUCE_PASSWORD, "Username is required"),
        (SAUCE_STANDARD_USER, "", "Password is required"),
    ],
    ids=["wrong-password", "unknown-user", "empty-username", "empty-password"],
)
def test_invalid_login_shows_error(page, username, password, expected_error):
    login = SauceLoginPage(page).open()
    login.login(username, password)

    expect(login.error).to_contain_text(expected_error)
    expect(page).not_to_have_url(re.compile(r"/inventory\.html"))


def test_locked_out_user_cannot_log_in(page):
    login = SauceLoginPage(page).open()
    login.login(SAUCE_LOCKED_USER, SAUCE_PASSWORD)

    expect(login.error).to_contain_text("Sorry, this user has been locked out.")
