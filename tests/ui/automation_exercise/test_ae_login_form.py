import re

from playwright.sync_api import expect

from pages.automation_exercise.login_page import AELoginPage


def test_empty_email_is_blocked_by_browser_validation(page):
    login = AELoginPage(page).open()
    login.login("", "anything")

    assert login.email_validation_message() != ""
    expect(page).to_have_url(re.compile(r"/login$"))


def test_badly_formatted_email_is_rejected(page):
    login = AELoginPage(page).open()
    login.login("not-an-email", "anything")

    assert login.email.evaluate("el => el.validity.typeMismatch") is True
    expect(page).to_have_url(re.compile(r"/login$"))


def test_wrong_credentials_show_error(page):
    login = AELoginPage(page).open()
    login.login("nobody_qa_test@example.com", "wrong-password")

    expect(login.error).to_be_visible()
    expect(login.logged_in_as).to_have_count(0)
