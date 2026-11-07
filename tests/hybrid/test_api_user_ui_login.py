"""Hybrid test: set up the data through the fast API, verify the behaviour through the real UI.

Signing up through the UI takes ~15 form fields and several pages. The API does
it in one request, so the UI test only spends time on what it actually checks: login.
"""
import re

from playwright.sync_api import expect

from pages.automation_exercise.login_page import AELoginPage


def test_user_created_via_api_can_log_in_via_ui(api_user, page):
    login = AELoginPage(page).open()
    login.login(api_user["email"], api_user["password"])

    expect(login.logged_in_as).to_contain_text(api_user["name"])
    expect(page).not_to_have_url(re.compile(r"/login$"))
