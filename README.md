# Cryptocurrency Market API

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [API Endpoints](#api-endpoints)
- [Documentation](#documentation)
- [Error Handling](#error-handling)
- [Unit Tests](#unit-tests)
- [Installation](#installation)
- [API Reference](docs/api.md)
- [Examples Guide](docs/examples.md)

## Overview

This document outlines the architecture and implementation plan for a REST API that provides cryptocurrency market updates. The API fetches data from the CoinGecko API and exposes endpoints to list coins, categories, and specific coin details.

## Project Structure

```
coin-api/
├── src/
│   ├── services/        # Business logic and data fetching from CoinGecko
│   ├── models/          # Data models using Pydantic
│   ├── middlewares/     # Custom middlewares
│   ├── utils/          # Utility functions (pagination, etc.)
│   ├── tests/          # Unit tests
│   └── main.py         # FastAPI application and endpoints
├── docs/              # API documentation
│   ├── api.md         # API reference
│   └── examples.md    # Usage examples
├── requirements.txt   # Project dependencies
├── README.md         # Project documentation
└── .gitignore       # Git ignore file
```

## Technology Stack

- **Language:** Python
- **Framework:** FastAPI
- **API Client:** `requests` library
- **Documentation:**
  - Swagger/OpenAPI (built into FastAPI)
  - Markdown documentation with examples
- **Testing:** `pytest`
- **Pagination:** Implemented for lists with configurable page size
- **Version Control:** Git

## API Endpoints

- **GET /** - Root endpoint

  - Response: Welcome message and API info

- **GET /api/v1/health** - Health check endpoint

  - Response: API health status

- **GET /api/v1/docs** - Interactive Swagger documentation

  - Response: Swagger UI for API exploration and testing

- **GET /api/v1/redoc** - ReDoc documentation

  - Response: Alternative API documentation viewer

- **GET /api/v1/coins** - List all coins (paginated)

  - Query parameters:
    - `page` (default: 1)
    - `per_page` (default: 10, max: 100)
  - Response: Paginated list of coins with market data

- **GET /api/v1/categories** - List coin categories

  - Response: List of all available cryptocurrency categories

- **GET /api/v1/coins/{coin_id}** - Get specific coin details

  - Path parameter: `coin_id`
  - Response: Detailed coin data including market data and links

- **GET /api/v1/categories/{category_id}/coins** - List coins by category
  - Path parameter: `category_id`
  - Query parameters:
    - `page` (default: 1)
    - `per_page` (default: 10, max: 100)
  - Response: Paginated list of coins in the category with market data

## Documentation

The API documentation is available in three formats:

1. **Swagger UI** (`/api/v1/docs`):

   - Interactive API documentation
   - Built-in request builder
   - Try out endpoints directly in the browser
   - OpenAPI specification

2. **ReDoc** (`/api/v1/redoc`):

   - Alternative documentation viewer
   - Clean, responsive interface
   - Search functionality

3. **API Reference** (`docs/api.md`):

   - Detailed endpoint documentation
   - Request/response formats
   - Status codes and error handling

4. **Examples Guide** (`docs/examples.md`):
   - cURL examples
   - Python code samples
   - JavaScript code samples
   - Best practices

## Error Handling

The API uses conventional HTTP response codes:

- `200 OK` - Request succeeded
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - CoinGecko API unavailable

All error responses include a JSON body with a detail message.

## Unit Tests

Comprehensive unit tests are written using `pytest` covering:

- API endpoints and responses
- Service layer and CoinGecko integration
- Pagination and error handling
- Category and coin data processing

Run tests with:

```bash
pytest
```

## Installation

### Docker

1. Build and run the Docker container using Docker Compose:

   ```bash
   docker compose up
   ```

   The API will be available at `http://localhost:8000`.

### Local Install

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the API:

   ```bash
   python -m src.main
   ```

   The API will be available at `http://localhost:8000`.
