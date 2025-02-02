"""Tests for coingecko service"""

from unittest.mock import patch, Mock
import requests
import pytest
from fastapi import HTTPException


class TestCoinGeckoService:
    """Tests for the CoinGeckoService class."""

    def test_service_initialization(self, service):
        """test service initialization"""
        assert service.base_url == "https://api.coingecko.com/api/v3"
        assert service.default_currency == "cad"
        assert "X-CG-Demo-API-Key" in service.headers

    @patch("requests.get")
    def test_make_request_success(self, mock_get, service, mock_response):
        """
        Tests the _make_request method with a successful API call.
        """
        mock_get.return_value = mock_response
        result = service._make_request("test-endpoint")
        assert result == {}
        mock_get.assert_called_once_with(
            "https://api.coingecko.com/api/v3/test-endpoint",
            params=None,
            headers=service.headers,
            timeout=200,
        )

    @patch("requests.get")
    def test_make_request_rate_limit(self, mock_get, service):
        """
        Tests the _make_request method when a rate limit error occurs.
        """
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=Mock(status_code=429)
        )
        mock_get.return_value = mock_response

        with pytest.raises(HTTPException) as exc_info:
            service._make_request("test-endpoint")
        assert exc_info.value.status_code == 429
        assert "Rate limit exceeded" in str(exc_info.value.detail)

    @patch("requests.get")
    def test_get_coins_list_success(self, mock_get, service, mock_coin_data):
        """
        Tests the get_coins_list method with a successful API call.
        """
        mock_response = Mock()
        mock_response.json.return_value = [mock_coin_data]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = service.get_coins_list()
        assert len(result) == 1
        assert result[0]["id"] == "bitcoin"
        assert result[0]["symbol"] == "btc"

    @patch("requests.get")
    def test_get_coins_list_with_pagination(self, mock_get, service):
        """Testing get_coins_list with pagination."""
        mock_coins = [{"id": f"coin{i}"} for i in range(15)]
        mock_response = Mock()
        mock_response.json.return_value = mock_coins
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = service.get_coins_list(page=1, per_page=10)
        assert len(result) == 10
        assert result[0]["id"] == "coin0"

    @patch("requests.get")
    def test_get_coin_categories_success(self, mock_get, service):
        """Testing get_coin_categories with a successful API call."""
        mock_categories = [
            {"category_id": "defi", "name": "DeFi"},
            {"category_id": "nft", "name": "NFT"},
        ]
        mock_response = Mock()
        mock_response.json.return_value = mock_categories
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = service.get_coin_categories()
        assert len(result) == 2
        assert result[0].id == "defi"
        assert result[1].id == "nft"

    @patch("requests.get")
    def test_get_coin_by_id_success(self, mock_get, service):
        """Testing get_coin_by_id with a successful API call."""
        mock_coin = {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "market_data": {
                "current_price": {"cad": 50000.0},
                "market_cap": {"cad": 1000000000.0},
                "price_change_24h": 1000.0,
                "price_change_percentage_24h": 2.5,
            },
            "links": {
                "homepage": ["https://bitcoin.org"],
                "blockchain_site": ["https://blockchain.info"],
                "official_forum_url": ["https://bitcointalk.org"],
            },
        }
        mock_response = Mock()
        mock_response.json.return_value = mock_coin
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = service.get_coin_by_id("bitcoin")
        assert result["id"] == "bitcoin"
        assert result["symbol"] == "btc"
        assert result["current_price"] == 50000.0
        assert "links" in result
        assert "homepage" in result["links"]

    @patch("requests.get")
    def test_get_coin_by_id_not_found(self, mock_get, service):
        """Testing get_coin_by_id when the coin is not found."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=Mock(status_code=404, json=lambda: {"detail": "Coin not found"})
        )
        mock_get.return_value = mock_response

        with pytest.raises(HTTPException) as exc_info:
            service.get_coin_by_id("invalid-coin")
        assert exc_info.value.status_code == 404

    @patch("requests.get")
    def test_get_coins_by_category_success(self, mock_get, service):
        """Testing get_coins_by_category with a successful API call."""

        mock_category = {"name": "DeFi Ecosystem"}

        mock_coins = [
            {
                "id": "uniswap",
                "symbol": "uni",
                "name": "Uniswap",
                "current_price": 5.0,
                "market_cap": 1000000.0,
                "market_cap_rank": 10,
                "price_change_24h": 0.5,
                "price_change_percentage_24h": 1.0,
            }
        ]

        mock_get.side_effect = [
            Mock(json=lambda: mock_category, raise_for_status=lambda: None),
            Mock(json=lambda: mock_coins, raise_for_status=lambda: None),
        ]

        result = service.get_coins_by_category("defi")
        assert result["category"] == "DeFi Ecosystem"
        assert len(result["coins"]) == 1
        assert result["coins"][0]["id"] == "uniswap"

    @patch("requests.get")
    def test_get_coins_by_category_with_pagination(self, mock_get, service):
        """Testing get_coins_by_category with pagination."""

        mock_category = {"name": "DeFi Ecosystem"}

        mock_coins = [{"id": f"coin{i}"} for i in range(2)]

        mock_get.side_effect = [
            Mock(json=lambda: mock_category, raise_for_status=lambda: None),
            Mock(json=lambda: mock_coins, raise_for_status=lambda: None),
        ]

        result = service.get_coins_by_category("defi", page=2, per_page=2)
        assert result["category"] == "DeFi Ecosystem"
        assert len(result["coins"]) == 2

    @patch("requests.get")
    def test_get_coins_by_category_not_found(self, mock_get, service):
        """Testing get_coins_by_category when the category is not found."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            response=Mock(
                status_code=404, json=lambda: {"detail": "Category not found"}
            )
        )
        mock_get.return_value = mock_response

        with pytest.raises(HTTPException) as exc_info:
            service.get_coins_by_category("invalid-category")
        assert exc_info.value.status_code == 404

    @patch("requests.get")
    def test_handle_network_error(self, mock_get, service):
        """Testing _make_request when a network error occurs."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with pytest.raises(HTTPException) as exc_info:
            service._make_request("test-endpoint")
        assert exc_info.value.status_code == 503
        assert "Error fetching data from CoinGecko" in str(exc_info.value.detail)

    @patch("requests.get")
    def test_make_request_request_exception(self, mock_get, service):
        """Testing _make_request when a request exception occurs."""
        mock_get.side_effect = requests.exceptions.RequestException("Timeout")

        with pytest.raises(HTTPException) as exc_info:
            service._make_request("test-endpoint")
        assert exc_info.value.status_code == 503
        assert "Error fetching data from CoinGecko" in str(exc_info.value.detail)

    @patch("requests.get")
    def test_get_coins_list_empty_response(self, mock_get, service):
        """Testing get_coins_list with an empty response."""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = service.get_coins_list()
        assert result == []

    @patch("requests.get")
    def test_get_coins_list_exception(self, mock_get, service):
        """Testing get_coins_list when an exception occurs."""
        mock_get.side_effect = Exception("Test exception")

        with pytest.raises(HTTPException) as exc_info:
            service.get_coins_list()
        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value.detail)

    @patch("requests.get")
    def test_get_coin_categories_empty_response(self, mock_get, service):
        """Testing get_coin_categories with an empty response."""
        mock_response = Mock()
        mock_response.json.return_value = "not a list"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = service.get_coin_categories()
        assert result == []

    @patch("requests.get")
    def test_get_coin_categories_exception(self, mock_get, service):
        """Testing get_coin_categories when an exception occurs."""
        mock_get.side_effect = Exception("Test exception")

        with pytest.raises(HTTPException) as exc_info:
            service.get_coin_categories()
        assert exc_info.value.status_code == 500
        assert "Internal server error" in str(exc_info.value.detail)

    @patch("requests.get")
    def test_get_coin_by_id_exception(self, mock_get, service):
        """Testing get_coin_by_id when an exception occurs."""
        mock_get.side_effect = Exception("Test exception")

        with pytest.raises(HTTPException) as exc_info:
            service.get_coin_by_id("bitcoin")
        assert exc_info.value.status_code == 404
        assert "Coin not found" in str(exc_info.value.detail)

    @patch("requests.get")
    def test_get_coins_by_category_empty_category_data(self, mock_get, service):
        """Testing get_coins_by_category with an empty category data."""
        mock_response = Mock()
        mock_response.json.return_value = None
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = service.get_coins_by_category("defi")
        assert result["category"] == "defi"
        assert result["coins"] == []

    @patch("requests.get")
    def test_get_coins_by_category_exception(self, mock_get, service):
        """Testing get_coins_by_category when an exception occurs."""
        mock_get.side_effect = Exception("Test exception")

        with pytest.raises(HTTPException) as exc_info:
            service.get_coins_by_category("defi")
        assert exc_info.value.status_code == 500
        assert "Error fetching category coins" in str(exc_info.value.detail)
