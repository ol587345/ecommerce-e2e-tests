"""Central place for URLs and credentials. Override any value with an environment variable."""
import os

AE_BASE_URL = os.getenv("AE_BASE_URL", "https://automationexercise.com")
AE_API_URL = os.getenv("AE_API_URL", f"{AE_BASE_URL}/api")

SAUCE_BASE_URL = os.getenv("SAUCE_BASE_URL", "https://www.saucedemo.com")
SAUCE_PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
SAUCE_STANDARD_USER = "standard_user"
SAUCE_LOCKED_USER = "locked_out_user"

# Third-party ad/consent hosts on Automation Exercise. Their pop-ups (e.g. the
# "#google_vignette" interstitial) randomly cover the page and are the #1 cause
# of flaky UI tests on this site, so we abort those requests at the network level.
BLOCKED_HOSTS = (
    "googlesyndication.com",
    "googleads.g.doubleclick.net",
    "doubleclick.net",
    "adservice.google.com",
    "fundingchoicesmessages.google.com",
    "googletagmanager.com",
    "google-analytics.com",
)

DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "15000"))
API_TIMEOUT_S = int(os.getenv("API_TIMEOUT_S", "30"))
