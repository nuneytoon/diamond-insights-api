# Diamond Insights API

A FastAPI-based backend service that retrieves baseball statistics daily from API Sports and provides endpoints to support the Diamond Insights React frontend application. This API layer processes and serves sports data to enable insightful visualizations and analytics.

## Features

- **Data Retrieval**: Automated daily fetching of baseball statistics from API Sports
- **RESTful API**: Clean, documented endpoints for the frontend application
- **FastAPI Framework**: Modern, fast, and easy-to-use Python web framework
- **Type Safety**: Full Pydantic validation for request/response models

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd diamond-insights-api
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (if needed)
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Running the Application

### Development Server

Start the FastAPI development server with hot-reload:

```bash
fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000`

### Production Server

Run with Uvicorn in production mode:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Running Tests

Run the test suite using pytest:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app tests/
```

## Project Structure

```
diamond-insights-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/          # API endpoints
│   │       ├── __init__.py
│   │       └── health.py
│   └── core/
│       ├── __init__.py
│       └── config.py        # Configuration settings
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
└── README.md

```

## Available Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Development

This project uses:
- **FastAPI** for the web framework
- **Pydantic** for data validation
- **Uvicorn** as the ASGI server

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
