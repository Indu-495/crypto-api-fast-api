"""
This module defines the main FastAPI application for the Cryptocurrency Market API.
"""

import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.services.coingecko_service import coingecko_service
from src.models.coin import CoinList, CategoryList, CoinDetail, CategoryCoins
from src.utils.pagination import validate_pagination_params

app = FastAPI(
    title="Cryptocurrency Market API",
    description="API for fetching cryptocurrency market updates",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10
MAX_PER_PAGE = 100


@app.get("/")
async def root():
    """
    Root endpoint for the API.
    """
    return {
        "message": "Welcome to Cryptocurrency Market API",
        "version": "1.0.0",
        "documentation": "/api/v1/docs",
    }


@app.get("/api/v1/health")
async def health_check():
    """
    Health check endpoint for the API.
    """
    return {"status": "healthy"}


@app.get("/api/v1/coins", response_model=CoinList)
async def list_coins(
    page: int = Query(DEFAULT_PAGE, ge=1, description="Page number"),
    per_page: int = Query(
        DEFAULT_PER_PAGE, ge=1, le=MAX_PER_PAGE, description="Items per page"
    ),
):
    """
    Lists all coins with pagination.

    - **page**: Page number (starts from 1)
    - **per_page**: Number of items per page (max 100)
    """
    page, per_page = validate_pagination_params(page, per_page, MAX_PER_PAGE)
    coins = coingecko_service.get_coins_list(page, per_page)

    total = (page * per_page) + per_page if coins else page * per_page

    return {"page": page, "per_page": per_page, "total": total, "items": coins}


@app.get("/api/v1/categories", response_model=CategoryList)
async def list_categories():
    """
    Lists all coin categories.
    """
    categories = coingecko_service.get_coin_categories()
    return {"categories": categories}


@app.get("/api/v1/coins/{coin_id}", response_model=CoinDetail)
async def get_coin(coin_id: str):
    """
    Gets detailed information about a specific coin.

    - **coin_id**: The ID of the coin to retrieve
    """
    try:
        return coingecko_service.get_coin_by_id(coin_id)
    except Exception as e:
        raise e


@app.get("/api/v1/categories/{category_id}/coins", response_model=CategoryCoins)
async def get_coins_by_category(
    category_id: str,
    page: int = Query(DEFAULT_PAGE, ge=1, description="Page number"),
    per_page: int = Query(
        DEFAULT_PER_PAGE, ge=1, le=MAX_PER_PAGE, description="Items per page"
    ),
):
    """
    Gets a list of coins for a specific category.

    - **category_id**: The ID of the category
    - **page**: Page number (starts from 1)
    - **per_page**: Number of items per page (max 100)
    """
    page, per_page = validate_pagination_params(page, per_page, MAX_PER_PAGE)
    try:
        return coingecko_service.get_coins_by_category(category_id, page, per_page)
    except Exception as e:
        raise e


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
