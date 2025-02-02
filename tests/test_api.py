from unittest.mock import patch
from fastapi import HTTPException


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "version" in response.json()


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


class TestCoinsEndpoints:
    @patch("src.services.coingecko_service.CoinGeckoService.get_coins_list")
    def test_list_coins_success(self, mock_get_coins, client, mock_coin_data):
        mock_get_coins.return_value = [mock_coin_data]
        response = client.get("/api/v1/coins")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "page" in data
        assert "per_page" in data
        assert "total" in data
        assert len(data["items"]) == 1
        assert data["items"][0]["id"] == mock_coin_data["id"]

    @patch("src.services.coingecko_service.CoinGeckoService.get_coins_list")
    def test_list_coins_with_pagination(
        self, mock_get_coins, client, mock_paginated_coin_response
    ):
        mock_get_coins.return_value = mock_paginated_coin_response["items"]
        response = client.get("/api/v1/coins?page=1&per_page=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["per_page"] == 10
        assert len(data["items"]) == 10

    @patch("src.services.coingecko_service.CoinGeckoService.get_coins_list")
    def test_list_coins_empty_page(self, mock_get_coins, client):
        mock_get_coins.return_value = []
        response = client.get("/api/v1/coins?page=999")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []


class TestCategoriesEndpoints:
    @patch("src.services.coingecko_service.CoinGeckoService.get_coin_categories")
    def test_list_categories_success(
        self, mock_get_categories, client, mock_category_data
    ):
        mock_get_categories.return_value = [mock_category_data]
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert len(data["categories"]) == 1
        assert data["categories"][0]["id"] == mock_category_data["id"]


class TestCoinDetailsEndpoint:
    @patch("src.services.coingecko_service.CoinGeckoService.get_coin_by_id")
    def test_get_coin_details_success(self, mock_get_coin, client, mock_coin_data):
        mock_get_coin.return_value = mock_coin_data
        response = client.get(f"/api/v1/coins/{mock_coin_data['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == mock_coin_data["id"]

    @patch("src.services.coingecko_service.CoinGeckoService.get_coin_by_id")
    def test_get_coin_details_not_found(self, mock_get_coin, client):
        mock_get_coin.side_effect = HTTPException(
            status_code=404, detail="Coin not found"
        )
        response = client.get("/api/v1/coins/invalid-coin")
        assert response.status_code == 404


class TestCategoryCoinsEndpoint:
    @patch("src.services.coingecko_service.CoinGeckoService.get_coins_by_category")
    def test_get_category_coins_success(
        self, mock_get_category_coins, client, mock_paginated_category_coins
    ):
        mock_get_category_coins.return_value = mock_paginated_category_coins
        response = client.get("/api/v1/categories/defi/coins")
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == mock_paginated_category_coins["category"]
        assert len(data["coins"]) == len(mock_paginated_category_coins["coins"])

    @patch("src.services.coingecko_service.CoinGeckoService.get_coins_by_category")
    def test_get_category_coins_pagination(
        self, mock_get_category_coins, client, mock_paginated_category_coins
    ):
        mock_get_category_coins.return_value = mock_paginated_category_coins
        response = client.get("/api/v1/categories/defi/coins?page=2&per_page=20")
        assert response.status_code == 200
        data = response.json()
        assert "category" in data
        assert "coins" in data
