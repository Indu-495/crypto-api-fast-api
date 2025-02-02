"""
This module provides a service for interacting with the CoinGecko API.
"""

import os
from typing import Optional, Dict, List
import requests
from fastapi import HTTPException
from dotenv import load_dotenv
from src.models.coin import Category


load_dotenv()


class CoinGeckoService:
    """
    A service for interacting with the CoinGecko API.
    """

    def __init__(self):
        """
        Initializes the CoinGeckoService with the base URL, default currency, and API key.
        """
        self.base_url = os.getenv("COINGECKO_API_URL")
        self.default_currency = os.getenv("DEFAULT_CURRENCY")
        self.api_key = os.getenv("API_KEY")
        self.headers = {"X-CG-Demo-API-Key": self.api_key}

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Makes a request to the CoinGecko API.

        Args:
            endpoint (str): The API endpoint to request.
            params (Optional[Dict], optional): The query parameters for the request.
            Defaults to None.

        Returns:
            Dict: The JSON response from the API.

        Raises:
            HTTPException: If the API request fails.
        """
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                headers=self.headers,
                timeout=200,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later.",
                ) from e
            raise HTTPException(
                status_code=e.response.status_code, detail=str(e)
            ) from e
        except requests.RequestException as e:
            raise HTTPException(
                status_code=503, detail=f"Error fetching data from CoinGecko: {str(e)}"
            ) from e

    def get_coins_list(self, page: int = 1, per_page: int = 10) -> List[Dict]:
        """
        Gets a list of all supported coins with pagination.

        Args:
            page (int, optional): The page number. Defaults to 1.
            per_page (int, optional): The number of items per page. Defaults to 10.

        Returns:
            List[Dict]: A list of dictionaries containing coin information.

        Raises:
            HTTPException: If the API request fails.
        """
        try:
            params = {
                "vs_currency": self.default_currency,
                "order": "market_cap_desc",
                "per_page": per_page + 1,
                "page": page,
                "sparkline": False,
            }

            data = self._make_request("coins/markets", params)

            if not data:
                return []

            data = data[:per_page]

            return [
                {
                    "id": coin.get("id"),
                    "symbol": coin.get("symbol"),
                    "name": coin.get("name"),
                    "current_price": coin.get("current_price"),
                    "market_cap": coin.get("market_cap"),
                    "market_cap_rank": coin.get("market_cap_rank"),
                    "price_change_24h": coin.get("price_change_24h"),
                    "price_change_percentage_24h": coin.get(
                        "price_change_percentage_24h"
                    ),
                }
                for coin in data
            ]

        except HTTPException as e:
            raise e from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            ) from e

    def get_coin_categories(self) -> List[Category]:
        """
        Gets a list of all coin categories.

        Returns:
            List[Category]: A list of Category objects.

        Raises:
            HTTPException: If the API request fails.
        """
        try:
            data = self._make_request("coins/categories/list")
            if not isinstance(data, list):
                return []

            categories = []
            for category in data:
                if isinstance(category, dict):
                    categories.append(Category.from_coingecko(category))
            return categories
        except HTTPException as e:
            raise e from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(e)}"
            ) from e

    def get_coin_by_id(self, coin_id: str) -> Dict:
        """
        Gets current data for a coin by its ID.

        Args:
            coin_id (str): The ID of the coin to retrieve.

        Returns:
            Dict: A dictionary containing detailed coin information.

        Raises:
            HTTPException: If the API request fails or the coin is not found.
        """
        params = {
            "vs_currency": self.default_currency,
            "localization": False,
            "tickers": False,
            "market_data": True,
            "community_data": False,
            "developer_data": False,
            "sparkline": False,
        }
        try:
            data = self._make_request(f"coins/{coin_id}", params)
            return {
                "id": data.get("id"),
                "symbol": data.get("symbol"),
                "name": data.get("name"),
                "current_price": data.get("market_data", {})
                .get("current_price", {})
                .get(self.default_currency),
                "market_cap": data.get("market_data", {})
                .get("market_cap", {})
                .get(self.default_currency),
                "market_cap_rank": data.get("market_cap_rank"),
                "price_change_24h": data.get("market_data", {}).get("price_change_24h"),
                "price_change_percentage_24h": data.get("market_data", {}).get(
                    "price_change_percentage_24h"
                ),
                "description": data.get("description"),
                "categories": data.get("categories"),
                "links": {
                    "homepage": data.get("links", {}).get("homepage", []),
                    "blockchain_site": data.get("links", {}).get("blockchain_site", []),
                    "official_forum_url": data.get("links", {}).get(
                        "official_forum_url", []
                    ),
                },
            }
        except HTTPException as e:
            raise e from e
        except Exception as e:
            raise HTTPException(
                status_code=404, detail=f"Coin not found: {coin_id}"
            ) from e

    def get_coins_by_category(
        self, category_id: str, page: int = 1, per_page: int = 10
    ) -> Dict:
        """
        Gets a list of coins for a specific category.

        Args:
            category_id (str): The ID of the category to retrieve coins from.
            page (int, optional): The page number. Defaults to 1.
            per_page (int, optional): The number of items per page. Defaults to 10.

        Returns:
            Dict: A dictionary containing the category name and a list of coins.

        Raises:
            HTTPException: If the API request fails.
        """
        try:

            category_data = self._make_request(f"coins/categories/{category_id}")
            if not category_data:
                return {"category": category_id, "coins": []}

            params = {
                "vs_currency": self.default_currency,
                "category": category_id,
                "order": "market_cap_desc",
                "per_page": per_page,
                "page": page,
                "sparkline": False,
            }

            coins_data = self._make_request("coins/markets", params)

            category_coins = [
                {
                    "id": coin.get("id"),
                    "symbol": coin.get("symbol"),
                    "name": coin.get("name"),
                    "current_price": coin.get("current_price"),
                    "market_cap": coin.get("market_cap"),
                    "market_cap_rank": coin.get("market_cap_rank"),
                    "price_change_24h": coin.get("price_change_24h"),
                    "price_change_percentage_24h": coin.get(
                        "price_change_percentage_24h"
                    ),
                }
                for coin in coins_data
            ]

            return {
                "category": category_data.get("name", category_id),
                "coins": category_coins,
            }
        except HTTPException as e:
            raise e from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching category coins: {str(e)}"
            ) from e


coingecko_service = CoinGeckoService()
