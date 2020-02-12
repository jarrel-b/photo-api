from typing import Dict

import pytest


@pytest.fixture
def order_form(**kwargs) -> Dict:
    body = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john.smith@domain.com",
        "primary_phone": "555-555-5555",
        "address_line_one": "P Sherman 42 Wallaby Way",
        "city": "Sydney",
        "state_or_region": "New South Wales",
        "postal_code": 2000,
        "country": "AUS",
        "print_id": 1,
        "photo_id": 10,
    }
    body.update(kwargs)
    return body
