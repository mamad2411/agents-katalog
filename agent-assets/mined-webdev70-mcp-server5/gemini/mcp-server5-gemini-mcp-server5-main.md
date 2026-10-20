# GEMINI.md

## Project Overview

This project is a Python-based **MCP (Model Context Protocol) Server** that acts as a middleware between a large language model (like Gemini) and the official **USAspending.gov API v2**. Its primary purpose is to enable the AI to reliably and efficiently answer complex questions about U.S. federal government award spending, including contracts, grants, loans, and other financial assistance.

The server is designed to be robust and efficient, implementing features like:
- **Smart Query Routing:** Uses `router_rules.json` to select the most efficient USAspending endpoint, preferring pre-calculated rollups over large data queries.
- **Entity Resolution:** Converts natural language queries for agencies and recipients into canonical IDs for the API.
- **Caching:** Multi-tier in-memory caching for reference data (agencies, award types), entities, and common queries to improve performance.
- **Circuit Breaker:** Protects the upstream USAspending API and ensures graceful degradation when the API is under load or down.
- **Observability:** Provides detailed debugging information and structured logging for every request.

The architecture is built to run locally on macOS and be deployed to **Google Cloud Run** as a containerized, stateless service.

## Tool Catalog

The server exposes the following MCP tools for use by the AI:

- **`answer_award_spending_question`**: [Orchestrator] Intelligently answers natural language questions by planning and executing necessary tool calls.
- **`spending_rollups`**: Returns total spending or Top N breakdowns (by agency, recipient, location, etc.) without listing individual awards.
- **`award_search`**: Flexible search for individual awards with filtering and sorting support.
- **`award_explain`**: Detailed breakdown of a specific award, including summary, transactions, and subawards.
- **`agency_portfolio`**: Summary of an agency's spending profile, including top awards and recipients.
- **`recipient_profile`**: spending history and details for a specific recipient (Vendor/Grantee).
- **`idv_vehicle_bundle`**: Specialized lookup for IDVs (Indefinite Delivery Vehicles) and their child task orders.
- **`resolve_entities`**: Resolves natural language names to canonical Agency or Recipient IDs.
- **`bootstrap_catalog`**: Initializes/refreshes reference catalogs (Agencies, Award Types). Recommended at session start.
- **`data_freshness`**: Checks when the USAspending data was last updated.

## Building and Running

The project uses `uv` for Python package management.

### Local Development

The project provides a `Makefile` for common development tasks.

- **Linting:** `make lint`
- **Unit Tests:** `make unit`
- **Integration Tests:** `make integration` (Starts mock server and runs tests in Docker)
- **Start StdIO Server:** `make run-stdio`
- **Start HTTP Server:** `make run-http`

### Manual Commands (using `uv`)

#### Local Development (stdio transport)

This mode is for running the server as a local process that communicates over standard input/output.

1.  **Install dependencies:**
    ```bash
    uv sync
    ```

2.  **Linting and Formatting:**
    ```bash
    uv run ruff check .
    uv run ruff format .
    ```

3.  **Run tests:**
    ```bash
    # Unit tests only
    uv run pytest -m "unit"

    # Metrics/Performance tests
    uv run pytest -m "metrics"
    ```

4.  **Start the MCP server:**
    ```bash
    uv run python -m usaspending_mcp.stdio_server
    ```

### Local Development (HTTP transport)

This mode runs the server with a FastAPI web interface.

1.  **Start the HTTP server:**
    ```bash
    uv run uvicorn usaspending_mcp.http_app:app --host 127.0.0.1 --port 8080 --reload
    ```

2.  **Test health endpoints:**
    ```bash
    curl http://localhost:8080/healthz
    ```

### Integration Testing

Integration tests require the mock USAspending API running in Docker to provide deterministic responses.

```bash
docker compose --profile test up --build --exit-code-from tests
```

### Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t usaspending-mcp .
    ```

2.  **Run the container:**
    ```bash
    docker run -e PORT=8080 -p 8080:8080 usaspending-mcp
    ```

## Configuration

Environment variables are used for configuration. A `.env.example` file is provided as a template.

- `PORT`: Port for the HTTP server (default: 8080).
- `LOG_LEVEL`: Logging verbosity (`debug`, `info`, `warning`, `error`).
- `USASPENDING_BASE_URL`: URL for the USAspending API (default: `https://api.usaspending.gov/api/v2`).
- `USASPENDING_TIMEOUT_S`: Request timeout in seconds.
- `DEFAULT_SCOPE_MODE`: Default award scope (`all_awards`, `contracts_only`, `assistance_only`).
- `FASTMCP_STATELESS_HTTP`: Set to `true` for Cloud Run (stateless) or `false` for local SSE support.

## Development Conventions

- **Dependency Management:** All Python dependencies are managed in `pyproject.toml` and installed using `uv`.
- **Code Structure:**
  - `src/usaspending_mcp/`: Core application logic, router, and API client.
  - `src/usaspending_mcp/tools/`: Individual MCP tool implementations.
  - `mock_usaspending/`: A standalone FastAPI server that mocks USAspending endpoints for testing.
  - `scripts/`: Shell scripts for GCP deployment and automation.
- **Deployment:** The target environment is Google Cloud Run. Use `scripts/deploy_cloud_run.sh` for deployment.
- **Operations:** Detailed instructions for health checks, monitoring, and troubleshooting can be found in [docs/runbook.md](docs/runbook.md).

## Reference Documentation

- **[docs/apis.md](docs/apis.md)**: Detailed mapping of USAspending API endpoints, award type codes (Contracts, Grants, Loans), and recommended implementation patterns for "all awards" filtering.
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)**: Rapid onboarding guide for developers and contributors.
- **[docs/PromptGuide.txt](docs/PromptGuide.txt)**: History of development prompts and architectural evolution.
- **[docs/prd.md](docs/prd.md)**: Product Requirement Document.