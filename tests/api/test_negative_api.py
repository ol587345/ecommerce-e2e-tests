import pytest

NOT_SUPPORTED = "This request method is not supported."


@pytest.mark.parametrize(
    "method, endpoint",
    [
        ("POST", "productsList"),
        ("PUT", "brandsList"),
        ("DELETE", "verifyLogin"),
    ],
)
def test_wrong_http_method_returns_405(api, method, endpoint):
    result = api.call(method, endpoint)

    assert result.code == 405
    assert result.message == NOT_SUPPORTED


@pytest.mark.parametrize(
    "endpoint, data, expected_message",
    [
        ("searchProduct", {}, "Bad request, search_product parameter is missing in POST request."),
        ("verifyLogin", {"password": "x"}, "Bad request, email or password parameter is missing in POST request."),
        ("verifyLogin", {"email": "a@b.com"}, "Bad request, email or password parameter is missing in POST request."),
    ],
    ids=["search-no-term", "login-no-email", "login-no-password"],
)
def test_missing_parameter_returns_400(api, endpoint, data, expected_message):
    result = api.call("POST", endpoint, data=data)

    assert result.code == 400
    assert result.message == expected_message


def test_login_with_unknown_user_returns_404(api):
    result = api.verify_login("nobody_qa_test@example.com", "whatever")

    assert result.code == 404
    assert result.message == "User not found!"
