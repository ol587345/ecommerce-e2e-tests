from framework.data import new_user


def test_user_lifecycle_create_login_delete(api):
    user = new_user()

    created = api.create_account(user)
    assert created.code == 201
    assert created.message == "User created!"

    try:
        login = api.verify_login(user["email"], user["password"])
        assert login.code == 200
        assert login.message == "User exists!"

        details = api.get_user_by_email(user["email"])
        assert details.code == 200
        assert details.body["user"]["email"] == user["email"]
        assert details.body["user"]["name"] == user["name"]
    finally:
        deleted = api.delete_account(user["email"], user["password"])
    assert deleted.code == 200
    assert deleted.message == "Account deleted!"

    after_delete = api.verify_login(user["email"], user["password"])
    assert after_delete.code == 404


def test_cannot_create_duplicate_email(api, api_user):
    result = api.create_account(api_user)

    assert result.code == 400
    assert result.message == "Email already exists!"


def test_login_with_wrong_password(api, api_user):
    result = api.verify_login(api_user["email"], "definitely-wrong")

    assert result.code == 404
    assert result.message == "User not found!"
