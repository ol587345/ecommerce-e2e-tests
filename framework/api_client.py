"""Thin wrapper around the Automation Exercise public API.

Quirk worth knowing: this API almost always returns HTTP 200 and puts the *real*
status in the JSON body as "responseCode". Tests therefore assert on
`result.code`, not on `result.http_status`.
"""
from dataclasses import dataclass

import requests

from framework.config import AE_API_URL, API_TIMEOUT_S


@dataclass
class ApiResult:
    http_status: int
    body: dict

    @property
    def code(self) -> int:
        return self.body.get("responseCode")

    @property
    def message(self) -> str:
        return self.body.get("message", "")


class AutomationExerciseAPI:
    def __init__(self, base_url: str = AE_API_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def call(self, method: str, endpoint: str, **kwargs) -> ApiResult:
        """Send any request. Public so negative tests can use wrong methods on purpose."""
        response = self.session.request(
            method, f"{self.base_url}/{endpoint}", timeout=API_TIMEOUT_S, **kwargs
        )
        # The body is JSON even though the Content-Type header says text/html.
        return ApiResult(response.status_code, response.json())

    # --- Products ---
    def get_products(self) -> ApiResult:
        return self.call("GET", "productsList")

    def get_brands(self) -> ApiResult:
        return self.call("GET", "brandsList")

    def search_product(self, term: str) -> ApiResult:
        return self.call("POST", "searchProduct", data={"search_product": term})

    # --- Users ---
    def create_account(self, user: dict) -> ApiResult:
        return self.call("POST", "createAccount", data=user)

    def verify_login(self, email: str, password: str) -> ApiResult:
        return self.call("POST", "verifyLogin", data={"email": email, "password": password})

    def get_user_by_email(self, email: str) -> ApiResult:
        return self.call("GET", "getUserDetailByEmail", params={"email": email})

    def delete_account(self, email: str, password: str) -> ApiResult:
        return self.call("DELETE", "deleteAccount", data={"email": email, "password": password})
