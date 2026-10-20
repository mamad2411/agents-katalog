# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

USAspending MCP Server - A Model Context Protocol (MCP) server that enables LLMs to query federal award spending data from USAspending.gov. The server provides both HTTP (FastAPI) and stdio transports.

## Common Commands

```bash
# Install dependencies (uses uv package manager)
uv sync

# Run unit tests
make unit

# Run integration tests (requires Docker)
make integration

# Lint and format check
make lint

# Auto-fix lint errors
make lint-fix

# Run HTTP server (with hot reload)
make run-http

# Run stdio server (for Claude Desktop)
make run-stdio

# Run a single test file
uv run pytest tests/test_router.py -v

# Run tests matching a pattern
uv run pytest -k "test_spending" -v
```

## Architecture

### Transport Layer
- `http_app.py` - FastAPI application exposing `/healthz`, `/readyz`, and `/mcp` endpoints. The MCP protocol is mounted at `/mcp` using `mcp.streamable_http_app()`
- `stdio_server.py` - Stdio transport entry point for Claude Desktop integration

### Core Components
- `server.py` - FastMCP server initialization and tool registration. All 10 MCP tools are defined here as decorated functions that delegate to tool classes
- `router.py` - Question routing logic that parses natural language questions, extracts signals (intents, entities, award IDs), and routes to appropriate tools
- `router_rules.json` - Configuration for routing rules, budgets (max 5 API requests per question), caching TTLs, and design decisions
- `usaspending_client.py` - HTTP client wrapper for USAspending.gov API with retry logic (tenacity), circuit breaker pattern, and structured error handling
- `cache.py` - In-memory caching for reference data and resolved entities

### Tools (in `tools/` directory)
Each tool is a class with an `execute()` method:
- `bootstrap_catalog.py` - Loads reference catalogs (agencies, award types)
- `resolve_entities.py` - Resolves natural language to canonical entities
- `award_search.py` - Searches awards with filters
- `award_explain.py` - Gets details for a specific award
- `spending_rollups.py` - Aggregated spending by agency/recipient/state
- `recipient_profile.py` - Recipient details and spending summary
- `agency_portfolio.py` - Agency overview and top awards
- `idv_vehicle_bundle.py` - IDV (Indefinite Delivery Vehicle) details
- `data_freshness.py` - Checks data currency
- `answer_award_spending_question.py` - Orchestrator tool that uses the Router

### Key Design Patterns
- **Scope Mode**: Tools support `scope_mode` parameter (`all_awards`, `contracts_only`, `assistance_only`) inferred from question context
- **Budget Enforcement**: Max 5 USAspending API requests per question, 12s wall time, 200KB response size
- **Agency Type Inference**: Distinguishes "awarding agency" vs "funding agency" based on keywords

## Testing

- Unit tests in `tests/test_*.py` - use respx for mocking HTTP
- Integration tests in `tests/integration/` - require Docker via `docker compose --profile test`
- Test markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.metrics`
- Coverage minimum: 50% (configured in pyproject.toml)

## Environment Variables

- `USASPENDING_BASE_URL` - API base URL (default: https://api.usaspending.gov/api/v2)
- `USASPENDING_TIMEOUT_S` - Request timeout in seconds (default: 60)
- `USASPENDING_MAX_RETRIES` - Max retry attempts (default: 3)
- `PORT` - HTTP server port (default: 8080)
- `LOG_LEVEL` - Logging level (default: info)
