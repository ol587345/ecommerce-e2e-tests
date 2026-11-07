# ecommerce-e2e-tests

An end-to-end test suite for two demo shops, written with Python, pytest and Playwright.

- **UI tests:** run against [Sauce Demo](https://www.saucedemo.com) and [Automation Exercise](https://automationexercise.com). They cover login (valid, invalid and locked-out users), the cart, checkout, sorting, search and filtering, and form validation.
- **API tests:** run against the [Automation Exercise API](https://automationexercise.com/api_list). They cover the product and brand lists, search, and creating, logging in as and deleting a user. Negative cases include wrong HTTP methods, missing parameters and unknown users.
- **Hybrid test:** creates a user through the API, logs in as that user through the UI, then deletes the user through the API.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                 # all tests, HTML report in reports/report.html
pytest -m api          # API only
pytest -m ui --headed  # UI tests in a visible browser
```

## Layout

```
framework/   config, API client, fake-data factory
pages/       Page Objects for each site
tests/       ui/, api/, hybrid/ + shared fixtures in conftest.py
explanations/  plain-text walkthrough of every part of the project
```
