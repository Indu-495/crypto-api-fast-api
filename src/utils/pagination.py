"""
This module provides utility functions for pagination.
"""

from typing import List, Dict, TypeVar, Any

T = TypeVar("T")


def validate_pagination_params(
    page: int, per_page: int, max_per_page: int = 100
) -> tuple[int, int]:
    """
    Validates and normalizes pagination parameters.

    Args:
        page (int): The page number.
        per_page (int): The number of items per page.
        max_per_page (int, optional): The maximum number of items per page. Defaults to 100.

    Returns:
        tuple[int, int]: A tuple containing the validated page and per_page values.
    """
    page = max(page, 1)
    if per_page < 1:
        per_page = 10
    per_page = min(per_page, max_per_page)
    return page, per_page


def paginate_response(items: List[T], page: int, per_page: int) -> Dict[str, Any]:
    """
    Creates a paginated response from a list of items.

    Args:
        items (List[T]): The list of items to paginate.
        page (int): The page number.
        per_page (int): The number of items per page.

    Returns:
        Dict[str, Any]: A dictionary containing the paginated items,
        page number, per_page, and total number of items.
    """

    total_items = len(items)

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page

    paginated_items = items[start_idx:end_idx] if start_idx < total_items else []

    return {
        "page": page,
        "per_page": per_page,
        "total": total_items,
        "items": paginated_items,
    }
