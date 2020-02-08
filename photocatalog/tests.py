from django.test import Client


def test_top_level_path_returns_200():
    client = Client()
    expected = 200

    response = client.get("/")

    assert expected == response.status_code
