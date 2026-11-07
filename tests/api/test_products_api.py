PRODUCT_FIELDS = {"id", "name", "price", "brand", "category"}


def test_get_all_products(api):
    result = api.get_products()

    assert result.code == 200
    products = result.body["products"]
    assert len(products) > 0
    for product in products:
        assert PRODUCT_FIELDS <= product.keys(), f"Missing fields in {product}"


def test_get_all_brands(api):
    result = api.get_brands()

    assert result.code == 200
    assert all(b["brand"] for b in result.body["brands"])


def test_search_product_returns_matches(api):
    result = api.search_product("jeans")

    assert result.code == 200
    products = result.body["products"]
    assert products, "Search returned nothing"
    # The API matches on product name OR category, so check both.
    for p in products:
        assert "jeans" in (p["name"] + " " + p["category"]["category"]).lower(), p


def test_search_with_no_match_returns_empty_list(api):
    result = api.search_product("zzz_no_such_product_zzz")

    assert result.code == 200
    assert result.body["products"] == []
