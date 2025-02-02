# API Usage Examples

This document provides examples of how to use the Cryptocurrency Market API with different programming languages and tools.

## cURL Examples

### Get All Coins

```bash
curl -X GET "http://localhost:8000/api/v1/coins?page=1&per_page=10"
```

### Get Specific Coin

```bash
curl -X GET "http://localhost:8000/api/v1/coins/bitcoin"
```

### Get All Categories

```bash
curl -X GET "http://localhost:8000/api/v1/categories"
```

### Get Coins in Category

```bash
curl -X GET "http://localhost:8000/api/v1/categories/defi/coins?page=1&per_page=10"
```

## Python Examples

### Get All Coins

```python
import requests

def get_coins(page=1, per_page=10):
    response = requests.get(
        "http://localhost:8000/api/v1/coins",
        params={"page": page, "per_page": per_page}
    )
    return response.json()

# Example usage
coins = get_coins(page=1, per_page=10)
for coin in coins["items"]:
    print(f"{coin['name']} ({coin['symbol']}): ${coin['current_price']}")
```

### Get Specific Coin

```python
import requests

def get_coin_details(coin_id):
    response = requests.get(f"http://localhost:8000/api/v1/coins/{coin_id}")
    return response.json()

# Example usage
bitcoin = get_coin_details("bitcoin")
print(f"Bitcoin Price: ${bitcoin['current_price']}")
print(f"24h Change: {bitcoin['price_change_percentage_24h']}%")
```

### Get Category Coins with Error Handling

```python
import requests

def get_category_coins(category_id, page=1, per_page=10):
    try:
        response = requests.get(
            f"http://localhost:8000/api/v1/categories/{category_id}/coins",
            params={"page": page, "per_page": per_page}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Example usage
defi_coins = get_category_coins("defi", page=1, per_page=10)
if defi_coins:
    print(f"Category: {defi_coins['category']}")
    for coin in defi_coins['coins']:
        print(f"{coin['name']}: ${coin['current_price']}")
```

## JavaScript Examples

### Get All Coins

```javascript
async function getCoins(page = 1, perPage = 10) {
  try {
    const response = await fetch(
      `http://localhost:8000/api/v1/coins?page=${page}&per_page=${perPage}`
    );
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}

// Example usage with async/await
async function displayCoins() {
  const coins = await getCoins(1, 10);
  if (coins) {
    coins.items.forEach((coin) => {
      console.log(`${coin.name} (${coin.symbol}): $${coin.current_price}`);
    });
  }
}

displayCoins();
```

### Get Specific Coin with Error Handling

```javascript
async function getCoinDetails(coinId) {
  try {
    const response = await fetch(
      `http://localhost:8000/api/v1/coins/${coinId}`
    );
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}

// Example usage with async/await and error handling
async function displayCoinDetails(coinId) {
  const coin = await getCoinDetails(coinId);
  if (coin) {
    console.log(`
      Name: ${coin.name}
      Price: $${coin.current_price}
      24h Change: ${coin.price_change_percentage_24h}%
      Market Cap: $${coin.market_cap}
    `);
  }
}

displayCoinDetails("bitcoin");
```

### Interactive Category Browser

```javascript
// Fetch and display all categories, then allow selecting one to view its coins
async function browseCategoryCoins() {
  try {
    // Get all categories
    const categoriesResponse = await fetch(
      "http://localhost:8000/api/v1/categories"
    );
    const categoriesData = await categoriesResponse.json();

    console.log("Available Categories:");
    categoriesData.categories.forEach((category) => {
      console.log(`${category.id}: ${category.name}`);
    });

    // Get coins for a specific category (example with 'defi')
    const categoryId = "defi";
    const coinsResponse = await fetch(
      `http://localhost:8000/api/v1/categories/${categoryId}/coins?page=1&per_page=10`
    );
    const coinsData = await coinsResponse.json();

    console.log(`\nCoins in ${coinsData.category}:`);
    coinsData.coins.forEach((coin) => {
      console.log(`
        ${coin.name} (${coin.symbol})
        Price: $${coin.current_price}
        Market Cap Rank: ${coin.market_cap_rank}
      `);
    });
  } catch (error) {
    console.error("Error:", error);
  }
}

browseCategoryCoins();
```

## Error Handling Examples

Here's how to handle common errors in your applications:

### Python

```python
import requests
from requests.exceptions import RequestException

def safe_api_call(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("Resource not found")
        elif e.response.status_code == 429:
            print("Rate limit exceeded. Please wait before trying again")
        else:
            print(f"HTTP Error: {e}")
    except RequestException as e:
        print(f"Error making request: {e}")
    return None
```

### JavaScript

```javascript
async function safeApiCall(url) {
  try {
    const response = await fetch(url);

    if (response.status === 404) {
      console.error("Resource not found");
      return null;
    }

    if (response.status === 429) {
      console.error("Rate limit exceeded. Please wait before trying again");
      return null;
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}
```

These examples demonstrate common usage patterns and best practices when working with the API. Remember to:

1. Always handle errors appropriately
2. Use pagination parameters when fetching lists
3. Check response status codes
4. Parse JSON responses properly
5. Use async/await for cleaner asynchronous code in JavaScript
