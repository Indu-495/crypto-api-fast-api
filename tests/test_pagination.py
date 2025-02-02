from src.utils.pagination import validate_pagination_params, paginate_response


def test_validate_pagination_params():
    page, per_page = validate_pagination_params(1, 10, 100)
    assert page == 1
    assert per_page == 10

    page, per_page = validate_pagination_params(1, 200, 100)
    assert per_page == 100

    page, per_page = validate_pagination_params(0, 0, 100)
    assert page == 1
    assert per_page == 10


def test_paginate_response():
    items = list(range(25))

    response = paginate_response(items, 1, 10)
    assert response["page"] == 1
    assert response["per_page"] == 10
    assert response["total"] == 25
    assert len(response["items"]) == 10
    assert response["items"] == items[:10]

    response = paginate_response(items, 2, 10)
    assert response["page"] == 2
    assert response["per_page"] == 10
    assert response["total"] == 25
    assert len(response["items"]) == 10
    assert response["items"] == items[10:20]

    response = paginate_response(items, 3, 10)
    assert response["page"] == 3
    assert response["per_page"] == 10
    assert response["total"] == 25
    assert len(response["items"]) == 5
    assert response["items"] == items[20:25]

    response = paginate_response(items, 4, 10)
    assert response["page"] == 4
    assert response["per_page"] == 10
    assert response["total"] == 25
    assert len(response["items"]) == 0
    assert response["items"] == []

    response = paginate_response(items, 1, 5)
    assert response["page"] == 1
    assert response["per_page"] == 5
    assert response["total"] == 25
    assert len(response["items"]) == 5
    assert response["items"] == items[:5]

    response = paginate_response([], 1, 10)
    assert response["page"] == 1
    assert response["per_page"] == 10
    assert response["total"] == 0
    assert len(response["items"]) == 0
    assert response["items"] == []
