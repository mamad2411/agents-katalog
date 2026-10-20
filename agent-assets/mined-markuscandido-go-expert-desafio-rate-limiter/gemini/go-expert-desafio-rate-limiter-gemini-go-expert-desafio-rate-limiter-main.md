# Project Overview

This project is a high-performance rate limiter middleware for Go web servers. It supports limiting requests by IP address or API token, with Redis used for distributed and persistent rate limit tracking. The project is designed with a modular architecture, including a configuration layer, a storage layer with a strategy pattern, a core rate limiter, and middleware for easy integration with any Go HTTP server. It also includes structured logging in JSON format for better observability.

# Building and Running

## Using Docker

The recommended way to run the project is using Docker Compose.

*   **Start the services:**
    ```bash
    docker-compose up -d
    ```

*   **Stop the services:**
    ```bash
    docker-compose down
    ```

*   **View logs:**
    ```bash
    docker-compose logs -f rate-limiter
    ```

## Manual Setup

**Prerequisites:**

*   Go 1.25 or higher
*   Redis 6.0 or higher

**Installation and Running:**

1.  **Install dependencies:**
    ```bash
    go mod download
    ```

2.  **Create a `.env` file:**
    ```bash
    cp .env.example .env
    ```

3.  **Build the application:**
    ```bash
    go build -o rate-limiter .
    ```

4.  **Run the application:**
    ```bash
    ./rate-limiter
    ```

## Makefile Commands

The project includes a `Makefile` with several useful commands:

*   `make build`: Build the application.
*   `make run`: Run the application.
*   `make test`: Run all tests.
*   `make test-coverage`: Run tests with a coverage report.
*   `make docker-up`: Build the Docker image and start the containers.
*   `make docker-down`: Stop the containers.
*   `make lint`: Run the linter.
*   `make fmt`: Format the code.

# Development Conventions

*   **Configuration:** Configuration is managed through environment variables or a `.env` file. The `internal/config` package is responsible for loading the configuration.
*   **Storage:** The project uses a strategy pattern for storage, making it easy to swap out the storage backend. The default implementation uses Redis and is located in `internal/storage`.
*   **Logging:** Structured JSON logging is used for better observability. The `pkg/logger` package provides the logging functionality.
*   **Testing:** The project has unit and integration tests. Tests can be run using the `go test` command or the `make test` command.
*   **Middleware:** The rate-limiting functionality is implemented as an HTTP middleware in `internal/middleware`, making it easy to integrate with any Go web server.
