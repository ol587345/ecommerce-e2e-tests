import pytest


@pytest.mark.parametrize(
    "option, read_values, reverse",
    [
        ("az", "names", False),
        ("za", "names", True),
        ("lohi", "prices", False),
        ("hilo", "prices", True),
    ],
    ids=["name-a-to-z", "name-z-to-a", "price-low-to-high", "price-high-to-low"],
)
def test_sort_products(sauce_inventory, option, read_values, reverse):
    sauce_inventory.sort_by(option)

    shown = getattr(sauce_inventory, read_values)()  # .names() or .prices()
    assert shown == sorted(shown, reverse=reverse)
