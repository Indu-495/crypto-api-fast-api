# Cryptocurrency Market API Documentation

This document describes the endpoints available in the Cryptocurrency Market API.

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required. All endpoints are publicly accessible.

## Endpoints

### Root

```http
GET /
```

Returns basic API information and links to documentation.

**Response**

```json
{
  "message": "Welcome to Cryptocurrency Market API",
  "version": "1.0.0",
  "documentation": "/api/v1/docs"
}
```

### Health Check

```http
GET /api/v1/health
```

Returns the health status of the API.

**Response**

```json
{
  "status": "healthy"
}
```

### List Coins

```http
GET /api/v1/coins
```

Returns a paginated list of all coins.

**Parameters**

| Name     | Type    | Description                             |
| -------- | ------- | --------------------------------------- |
| page     | integer | Page number (starts from 1). Default: 1 |
| per_page | integer | Items per page (max 100). Default: 10   |

**Response**

```json
{
  "page": 1,
  "per_page": 10,
  "total": 20,
  "items": [
    {
      "id": "bitcoin",
      "symbol": "btc",
      "name": "Bitcoin",
      "current_price": 50000.0,
      "market_cap": 1000000000.0,
      "market_cap_rank": 1,
      "price_change_24h": 1000.0,
      "price_change_percentage_24h": 2.5
    }
  ]
}
```

### List Categories

```http
GET /api/v1/categories
```

Returns a list of all coin categories.

**Response**

```json
{
  "categories": [
    {
      "id": "defi",
      "name": "DeFi"
    },
    {
      "id": "nft",
      "name": "NFT"
    }
  ]
}
```

### Get Coin Details

```http
GET /api/v1/coins/{coin_id}
```

Returns detailed information about a specific coin.

**Parameters**

| Name    | Type   | Description                |
| ------- | ------ | -------------------------- |
| coin_id | string | ID of the coin to retrieve |

**Response**

```json
{
  "id": "bitcoin",
  "symbol": "btc",
  "name": "Bitcoin",
  "current_price": 50000.0,
  "market_cap": 1000000000.0,
  "market_cap_rank": 1,
  "price_change_24h": 1000.0,
  "price_change_percentage_24h": 2.5,
  "description": "Bitcoin is a decentralized cryptocurrency...",
  "categories": ["Store of Value", "PoW"],
  "links": {
    "homepage": ["https://bitcoin.org"],
    "blockchain_site": ["https://blockchain.info"],
    "official_forum_url": ["https://bitcointalk.org"]
  }
}
```

### Get Coins by Category

```http
GET /api/v1/categories/{category_id}/coins
```

Returns a paginated list of coins in a specific category.

**Parameters**

| Name        | Type    | Description                             |
| ----------- | ------- | --------------------------------------- |
| category_id | string  | ID of the category                      |
| page        | integer | Page number (starts from 1). Default: 1 |
| per_page    | integer | Items per page (max 100). Default: 10   |

**Response**

```json
{
  "category": "DeFi Ecosystem",
  "coins": [
    {
      "id": "uniswap",
      "symbol": "uni",
      "name": "Uniswap",
      "current_price": 5.0,
      "market_cap": 1000000.0,
      "market_cap_rank": 10,
      "price_change_24h": 0.5,
      "price_change_percentage_24h": 1.0
    }
  ]
}
```

## Error Handling

The API uses conventional HTTP response codes to indicate the success or failure of requests.

- `200 OK` - Request succeeded
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - CoinGecko API unavailable

Error responses include a detail message:

```json
{
  "detail": "Error message here"
}
```
