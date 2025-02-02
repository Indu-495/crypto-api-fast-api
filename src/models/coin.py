from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Coin(BaseModel):
    id: str
    symbol: str
    name: str
    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    market_cap_rank: Optional[int] = None
    price_change_24h: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None


class Category(BaseModel):
    id: str = ""  # Using category_id as id
    name: str

    @classmethod
    def from_coingecko(cls, data: Dict[str, Any]) -> "Category":
        return cls(id=data.get("category_id", ""), name=data.get("name", ""))


class PaginatedResponse(BaseModel):
    page: int
    per_page: int
    total: int
    items: List


class CoinList(PaginatedResponse):
    items: List[Coin]


class CategoryList(BaseModel):
    categories: List[Category]


class CoinDetail(Coin):
    description: Optional[Dict] = None
    categories: Optional[List[str]] = None
    links: Optional[Dict] = None


class CategoryCoins(BaseModel):
    category: str
    coins: List[Coin]
