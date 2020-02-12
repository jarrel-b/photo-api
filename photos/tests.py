import json

import pytest
from django.test import Client

from photocatalog import CURRENT_VERSION

from .data import DEFAULT_PAGE_SIZE
from .models import Catalog


@pytest.fixture
@pytest.mark.usefixtures("django_db_setup")
def clear_catalog():
    Catalog.objects.all().delete()


def test_empty_path_value_provides_default():
    item = Catalog()

    assert item.path is not None


@pytest.mark.django_db
@pytest.mark.usefixtures("django_db_setup")
def test_list_catalog_returns_200_status_code():
    client = Client()
    expected = 200

    response = client.get(f"/{CURRENT_VERSION}/catalog/")

    assert expected == response.status_code


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_catalog")
def test_list_catalog_empty_catalog_returns_empty_result_set():
    client = Client()
    expected = {"count": 0, "last_token": None, "results": []}

    response = client.get(f"/{CURRENT_VERSION}/catalog/")

    assert expected == json.loads(response.content)


@pytest.mark.django_db
@pytest.mark.usefixtures("clear_catalog")
def test_list_catalog_no_page_size_and_no_last_token_returns_all_results():
    for _ in range(10):
        item = Catalog()
        item.save()
    client = Client()
    expected = 10

    response = client.get(f"/{CURRENT_VERSION}/catalog/")

    response = json.loads(response.content)
    assert expected == len(response["results"]) == response["count"]


@pytest.mark.django_db
def test_list_catalog_last_token_is_expected():
    client = Client()

    response = client.get(f"/{CURRENT_VERSION}/catalog/")

    response = json.loads(response.content)
    assert response["last_token"] == response["results"][-1]["id"]


@pytest.mark.django_db
def test_list_catalog_page_size_but_no_last_token_returns_first_page():
    client = Client()
    page_size = 20
    expected = 20

    response = client.get(f"/{CURRENT_VERSION}/catalog/?page_size={page_size}")

    response = json.loads(response.content)
    assert expected == len(response["results"]) == response["count"]


@pytest.mark.django_db
def test_list_catalog_no_page_size_but_last_token_returns_next_page():
    client = Client()
    last_token = 20
    expected = DEFAULT_PAGE_SIZE

    response = client.get(
        f"/{CURRENT_VERSION}/catalog/?last_token={last_token}"
    )

    response = json.loads(response.content)
    assert expected == len(response["results"]) == response["count"]


@pytest.mark.django_db
def test_list_catalog_page_size_and_last_token_returns_next_page():
    client = Client()
    last_token = 20
    page_size = 10
    expected = 10

    response = client.get(
        f"/{CURRENT_VERSION}/catalog/?"
        f"last_token={last_token}&page_size={page_size}"
    )

    response = json.loads(response.content)
    assert expected == len(response["results"]) == response["count"]


@pytest.mark.django_db
def test_list_catalog_page_size_and_last_token_returns_expected():
    client = Client()
    last_token = 20
    page_size = 10

    response = client.get(
        f"/{CURRENT_VERSION}/catalog/?"
        f"last_token={last_token}&page_size={page_size}"
    )

    response = json.loads(response.content)
    for item in response["results"]:
        assert (
            item["id"] > last_token and item["id"] <= last_token + page_size
        ), f"Catalog item {item} should not be in this page"


@pytest.mark.django_db
def test_list_catalog_pagination_returns_all_results():
    client = Client()
    page_size = 20
    first = True
    last_token = "token"
    expected = 100
    results = []
    while first or last_token:
        if first:
            first = False

            response = client.get(
                f"/{CURRENT_VERSION}/catalog/?page_size={page_size}"
            )
        else:
            response = client.get(
                (
                    f"/{CURRENT_VERSION}/catalog/?"
                    f"page_size={page_size}&last_token={last_token}"
                )
            )
        response = json.loads(response.content)
        results += response["results"]
        last_token = response["last_token"]

    assert expected == len(results)
