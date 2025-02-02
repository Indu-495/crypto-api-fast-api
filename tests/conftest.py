from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient
from src.services.coingecko_service import CoinGeckoService
from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_coin_data():
    return {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "current_price": 50000.0,
        "market_cap": 1000000000.0,
        "market_cap_rank": 1,
        "price_change_24h": 1000.0,
        "price_change_percentage_24h": 2.5,
    }


@pytest.fixture
def mock_category_data():
    return {"id": "defi", "name": "DeFi"}


@pytest.fixture
def mock_paginated_coin_response(mock_coin_data):
    return {"page": 1, "per_page": 10, "total": 100, "items": [mock_coin_data] * 10}


@pytest.fixture
def mock_paginated_category_coins(mock_coin_data):
    return {"category": "DeFi", "coins": [mock_coin_data] * 10}


@pytest.fixture
def service():
    return CoinGeckoService()


@pytest.fixture
def mock_response():
    mock = Mock()
    mock.json.return_value = {}
    mock.raise_for_status.return_value = None
    return mock
