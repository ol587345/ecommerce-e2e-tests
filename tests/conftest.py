"""Shared fixtures. pytest loads this file automatically for every test under tests/."""
import base64
from pathlib import Path
from urllib.parse import urlparse

import pytest
import pytest_html

from framework.api_client import AutomationExerciseAPI
from framework.config import BLOCKED_HOSTS, DEFAULT_TIMEOUT_MS, SAUCE_PASSWORD, SAUCE_STANDARD_USER
from framework.data import new_user
from pages.saucedemo.inventory_page import InventoryPage
from pages.saucedemo.login_page import SauceLoginPage


def pytest_collection_modifyitems(items):
    """Tag each test with ui / api / hybrid based on its folder, so `pytest -m api` works."""
    for item in items:
        folder = Path(item.fspath).parts
        for marker in ("ui", "api", "hybrid"):
            if marker in folder:
                item.add_marker(marker)


_SCREENSHOTS = pytest.StashKey[list]()


def _capture(page) -> str:
    return base64.b64encode(page.screenshot(full_page=True)).decode()


@pytest.fixture
def screenshot(request, page):
    """Call screenshot("step name") inside a test to add a picture of the page to the HTML report."""
    shots = request.node.stash.setdefault(_SCREENSHOTS, [])

    def take(name: str):
        shots.append((name, _capture(page)))

    return take


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """After each browser test, add its step screenshots plus a final one to the HTML report."""
    report = yield
    page = item.funcargs.get("page")
    if report.when == "call" and page is not None:
        shots = item.stash.get(_SCREENSHOTS, [])
        shots.append(("failure" if report.failed else "end of test", _capture(page)))
        report.extras = getattr(report, "extras", []) + [
            pytest_html.extras.png(data, name) for name, data in shots
        ]
    return report


# pytest-html opens a clicked image with window.open(<data: URL>), which browsers block.
# This runs first and opens the image in a blank tab instead.
_OPEN_SCREENSHOT_IN_NEW_TAB = """<script>
document.addEventListener('click', (event) => {
    const image = event.target.closest('.media-container__viewport img');
    if (!image) return;
    event.stopPropagation();
    const tab = window.open('', '_blank');
    tab.document.title = image.closest('.media').querySelector('.media__name').innerText;
    const copy = tab.document.createElement('img');
    copy.src = image.src;
    tab.document.body.append(copy);
}, true);
</script>"""


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.append(_OPEN_SCREENSHOT_IN_NEW_TAB)


def _block_ads(route):
    host = urlparse(route.request.url).hostname or ""
    if any(host == h or host.endswith("." + h) for h in BLOCKED_HOSTS):
        route.abort()
    else:
        route.continue_()


@pytest.fixture(autouse=True)
def _browser_setup(request):
    """For browser tests only: block ad hosts and set the default timeout.
    API tests never ask for `page`, so no browser is started for them."""
    if "page" in request.fixturenames:
        context = request.getfixturevalue("context")
        context.set_default_timeout(DEFAULT_TIMEOUT_MS)
        context.route("**/*", _block_ads)
    yield


@pytest.fixture(scope="session")
def api() -> AutomationExerciseAPI:
    return AutomationExerciseAPI()


@pytest.fixture
def api_user(api):
    """Create a fresh user through the API, hand it to the test, then delete it."""
    user = new_user()
    result = api.create_account(user)
    assert result.code == 201, f"User setup failed: {result.body}"
    yield user
    api.delete_account(user["email"], user["password"])


@pytest.fixture
def sauce_inventory(page) -> InventoryPage:
    """Sauce Demo already logged in as standard_user, sitting on the products page."""
    SauceLoginPage(page).open().login(SAUCE_STANDARD_USER, SAUCE_PASSWORD)
    return InventoryPage(page)
