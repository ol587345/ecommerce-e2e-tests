"""Test-data factories. Every call returns a brand-new, unique user."""
import uuid

from faker import Faker

fake = Faker()


def new_user() -> dict:
    """All fields required by the createAccount API, filled with fake data."""
    first, last = fake.first_name(), fake.last_name()
    birth = fake.date_of_birth(minimum_age=18, maximum_age=70)
    return {
        "name": f"{first} {last}",
        # uuid guarantees uniqueness; Faker emails can collide with accounts left on the shared site.
        "email": f"qa_{uuid.uuid4().hex[:12]}@example.com",
        "password": fake.password(length=12),
        "title": fake.random_element(["Mr", "Mrs"]),
        "birth_date": str(birth.day),
        "birth_month": str(birth.month),
        "birth_year": str(birth.year),
        "firstname": first,
        "lastname": last,
        "company": fake.company(),
        "address1": fake.street_address(),
        "address2": "",
        "country": "United States",
        "zipcode": fake.postcode(),
        "state": fake.state(),
        "city": fake.city(),
        "mobile_number": fake.msisdn(),
    }
