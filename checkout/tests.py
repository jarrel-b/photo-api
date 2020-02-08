import json
import uuid
from datetime import datetime
from typing import Dict
from unittest import mock

import pytest
from django.test import Client

from photocatalog import CURRENT_VERSION
from photos.models import Catalog

from .data import DATETIME_FORMAT
from .models import Prints, Statuses


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


def test_checkout_empty_body_returns_422_status_code():
    client = Client()
    expected = 422

    response = client.post(f"/{CURRENT_VERSION}/checkout", {})

    assert expected == response.status_code


@pytest.mark.django_db
def test_checkout_body_missing_inputs_returns_422_status_code(order_form):
    client = Client()
    expected = 422
    order_form.pop("email")

    response = client.post(f"/{CURRENT_VERSION}/checkout", order_form)

    assert expected == response.status_code


@pytest.mark.django_db
def test_checkout_invalid_print_id_returns_422_status_code(order_form):
    client = Client()
    expected = 422
    order_form["print_id"] = "extra extra large"

    response = client.post(f"/{CURRENT_VERSION}/checkout", order_form)

    assert expected == response.status_code


@pytest.mark.django_db
def test_checkout_invalid_photo_id_returns_422_status_code(order_form):
    client = Client()
    expected = 422
    order_form["photo_id"] = "a-non-existent-photo"

    response = client.post(f"/{CURRENT_VERSION}/checkout", order_form)

    assert expected == response.status_code


@pytest.mark.django_db
def test_checkout_valid_body_returns_201_status_code(order_form):
    client = Client()
    expected = 201

    response = client.post(f"/{CURRENT_VERSION}/checkout", order_form)

    assert expected == response.status_code


@pytest.mark.django_db
@pytest.mark.usefixtures("django_db_setup")
def test_checkout_returns_correct_order_details(order_form):
    client = Client()
    now = datetime(2020, 1, 1)
    expected_address = order_form["address_line_one"]
    if order_form.get("address_line_two"):
        expected_address += " " + order_form["address_line_two"]
    fake_order_id = uuid.uuid4()
    expected = {
        "id": str(fake_order_id),
        "status": Statuses.CREATED.value,
        "placed_on": now.strftime(DATETIME_FORMAT),
        "items_ordered": [
            {
                "title": Catalog.objects.filter(id=order_form["photo_id"])[
                    0
                ].title,
                "size": Prints.objects.filter(id=order_form["print_id"])[
                    0
                ].size,
            }
        ],
        "shipping_summary": {
            "ship_to": " ".join(
                (order_form["first_name"], order_form["last_name"])
            ),
            "email": order_form["email"],
            "phone": order_form["primary_phone"],
            "address": expected_address,
            "city": order_form["city"],
            "state_or_region": order_form["state_or_region"],
            "postal_code": order_form["postal_code"],
            "country": order_form["country"],
        },
        "billing_summary": {
            "order_total": float(
                Prints.objects.filter(id=order_form["print_id"])[
                    0
                ].total_cost()
            ),
            "shipping_total": float(
                Prints.objects.filter(id=order_form["print_id"])[
                    0
                ].shipping_cost
            ),
            "item_total": float(
                Prints.objects.filter(id=order_form["print_id"])[0].print_cost
            ),
        },
    }
    with mock.patch(
        "checkout.models.timezone.now", autospec=True
    ) as mock_generate_now, mock.patch(
        "checkout.models.uuid.uuid4", autospec=True
    ) as mock_uuid_uuid4:
        mock_generate_now.side_effect = lambda: now
        mock_uuid_uuid4.side_effect = lambda: fake_order_id

        response = client.post(f"/{CURRENT_VERSION}/checkout", order_form)

    assert expected == json.loads(response.content)
