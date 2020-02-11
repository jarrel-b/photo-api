import json

import pytest

from photocatalog import CURRENT_VERSION
from photos.models import IMAGE_NOT_AVAILABLE_PATH, Catalog


def test_index_returns_200_status_Code(django_app):
    expected = 200
    response = django_app.get("/")

    assert expected == response.status_code


@pytest.mark.django_db
def test_list_catalog_returns_200_status_code(django_app):
    expected = 200
    response = django_app.get(f"/{CURRENT_VERSION}/catalog")

    assert expected == response.status_code


@pytest.mark.django_db
def test_list_catalog_does_not_change_catalog(django_app):
    expected = [row for row in Catalog.objects.all()]

    django_app.get(f"/{CURRENT_VERSION}/catalog")

    actual = [row for row in Catalog.objects.all()]
    assert expected == actual


@pytest.mark.django_db
@pytest.mark.usefixtures("django_db_setup")
def test_list_catalog_with_no_query_params_returns_all_results(django_app):
    Catalog.objects.all().delete()
    items = 10
    for _ in range(items):
        item = Catalog()
        item.save()
    expected = items

    response = django_app.get(f"/{CURRENT_VERSION}/catalog")

    response = json.loads(response.content)
    assert expected == len(response["results"]) == response["count"]


@pytest.mark.django_db
@pytest.mark.usefixtures("django_db_setup")
def test_list_catalog_with_no_query_params_returns_expected(django_app):
    last_row = Catalog.objects.order_by("-id").first()
    Catalog.objects.all().delete()
    items = 10
    for _ in range(items):
        item = Catalog()
        item.save()
    expected = {
        "count": items,
        "last_token": last_row.id + items,
        "results": [
            {
                "id": last_row.id + i,
                "title": None,
                "location": None,
                "year": None,
                "path": IMAGE_NOT_AVAILABLE_PATH,
            }
            for i in range(1, items + 1)
        ],
    }

    response = django_app.get(f"/{CURRENT_VERSION}/catalog")

    assert expected == json.loads(response.content)


@pytest.mark.django_db
@pytest.mark.usefixtures("django_db_setup")
def test_list_catalog_pagination_returns_all_items(django_app):
    last_row = Catalog.objects.order_by("-id").first()
    Catalog.objects.all().delete()
    items = 10
    for _ in range(items):
        item = Catalog()
        item.save()
    expected = 10
    page_size = 1
    last_token = last_row.id
    results = []
    while last_token:

        response = django_app.get(
            (
                f"/{CURRENT_VERSION}/catalog?"
                f"page_size={page_size}&last_token={last_token}"
            )
        )
        response = json.loads(response.content)
        results += response["results"]
        last_token = response["last_token"]

    assert expected == len(results)


@pytest.mark.django_db
@pytest.mark.usefixtures("django_db_setup")
def test_list_catalog_pagination_returns_expected(django_app):
    last_row = Catalog.objects.order_by("-id").first()
    Catalog.objects.all().delete()
    items = 10
    for _ in range(items):
        item = Catalog()
        item.save()
    expected = [
        {
            "id": row.id,
            "title": None,
            "location": None,
            "year": None,
            "path": IMAGE_NOT_AVAILABLE_PATH,
        }
        for row in Catalog.objects.all()
    ]
    page_size = 1
    last_token = last_row.id
    results = []
    while last_token:

        response = django_app.get(
            (
                f"/{CURRENT_VERSION}/catalog?"
                f"page_size={page_size}&last_token={last_token}"
            )
        )
        response = json.loads(response.content)
        results += response["results"]
        last_token = response["last_token"]

    assert expected == results
