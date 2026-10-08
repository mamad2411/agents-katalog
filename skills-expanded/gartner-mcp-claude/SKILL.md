# CLAUDE.md

This file provides guidance to Claude Code when working on this project.

## Project Overview

Gartner MCP is a Model Context Protocol server that provides programmatic access to Gartner.com research. It exposes tools for searching documents, reading full content, downloading PDFs, and using AskGartner AI.

## Architecture

- **MCP server** (`server.py`) — FastMCP tool definitions and client lifecycle management
- **Auth** (`auth.py`) — Playwright-based browser login; keeps the browser alive for document API calls
- **Documents** (`documents.py`) — Fetches documents and downloads PDFs via the live login browser
- **Search** (`search.py`) — Research search via Gartner's search API (httpx)
- **AskGartner** (`ask_gartner.py`) — AskGartner AI Q&A via SSE streaming (httpx)
- **HTTP client** (`http_client.py`) — Shared httpx client with persistent cookie jar
- **Config** (`config.py`) — API URLs, cookie/storage paths, default headers

### Key Design Decisions

**Browser-based document access:** The `www.gartner.com` document API is behind Cloudflare's managed challenge, which blocks httpx requests. The login browser (Playwright, headed) is kept alive after authentication and reused for all document/PDF API calls via `page.evaluate(fetch(...))`.

**Response interception:** When fetching documents, the code navigates to the document reader page and intercepts the API response that the page's own JavaScript makes. This captures the correct request headers, which are then reused for subsequent fetch() calls (user profile, PDF download).

**Separate HTTP paths:** Search and AskGartner use httpx (they hit different domains not behind Cloudflare). Documents use the live Playwright browser.

## Commands

```bash
# Install dependencies
uv sync

# Install Playwright browsers
uv run playwright install chromium

# Run the MCP server directly
uv run python -m gartner_mcp
```

## MCP Configuration

Add to Claude Code's `.mcp.json`:

```json
{
  "mcpServers": {
    "gartner": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/gartner-mcp", "python", "-m", "gartner_mcp"]
    }
  }
}
```

## File Layout

```
src/gartner_mcp/
  __init__.py       # Package marker
  __main__.py       # Entry point: python -m gartner_mcp
  server.py         # MCP tool definitions, client lifecycle
  auth.py           # Playwright login, cookie management
  documents.py      # Document fetch + PDF download (browser-based)
  search.py         # Research search (httpx)
  ask_gartner.py    # AskGartner AI streaming Q&A (httpx)
  http_client.py    # Shared httpx client with cookie jar
  config.py         # URLs, paths, constants
```

## State Files

- `~/.config/gartner-api/cookies.txt` — MozillaCookieJar for httpx clients
- `~/.config/gartner-api/storage_state.json` — Playwright storage state (cookies + localStorage)

## Important Notes

- Login opens a visible browser window (for CAPTCHA/MFA handling) that must stay open during the session
- The document API requires navigating to the document reader page to capture correct request headers
- PDFs are downloaded via base64-encoded fetch in the browser, decoded server-side
- Search hits `searchapi.pdo.aws.gartner.com` (no Cloudflare), documents hit `www.gartner.com` (Cloudflare-protected)
