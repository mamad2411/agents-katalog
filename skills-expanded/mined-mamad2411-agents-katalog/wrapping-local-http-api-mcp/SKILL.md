---
name: wrapping-local-http-api-mcp
description: "Turn any local app's HTTP API into an MCP server for Hermes Agent — reusable code template, config wiring, and pitfalls. For apps like Logseq, Trilium, or any daemon with a REST/JSON-RPC endpoint."
version: 1.0.0
metadata:
  hermes:
    triggers:
      - wrap http api as mcp
      - local http api mcp server
      - turn app api into mcp
      - logseq mcp integration
      - trilium mcp integration
      - rest api mcp wrapper
    tags: [mcp, http-api, integration, logseq, trilium, rest]
    related_skills: [building-mcp-servers, mcp-server-onboarding]
---

# Wrapping Local HTTP APIs as MCP Servers

Turn desktop/server apps that expose HTTP APIs into first-class MCP tools for Hermes Agent.

## When to Use

An app has a built-in HTTP API (REST, JSON-RPC, plain HTTP) that you want Hermes agents to call as tools. The app runs locally (or is reachable on the network). Examples: Logseq's JSON-RPC API, Trilium's ETAPI, any app with `curl`-accessible endpoints.

## API Discovery for Compiled/Minified Apps

When the app has no public docs, reverse-engineer its HTTP endpoints from bundled JS:

```bash
# Extract all route strings from a minified bundle
grep -o '"/api/[^"]*"' main.cjs | sort -u

# Or find method-specific patterns
grep -o '"POST [^"]*"' main.cjs | sort -u
grep -o '"/etapi/[^"]*"' main.cjs | sort -u
```

Then test each candidate with `curl` to confirm it works. This technique works on Electron apps, compiled Node servers, and Vite-bundled SPAs — the route strings survive minification because they're hash-constant runtime values.

## Token Injection for SQLite-Backed Services

Some apps (Trilium, some self-hosted tools) require a web UI to generate API tokens. When the UI is inaccessible (no browser, headless Docker), inject the token directly into SQLite:

```python
# In the Docker container or via sqlite3 CLI:
import sqlite3, hashlib, secrets, datetime

db = sqlite3.connect("/path/to/app.db")
raw_token = secrets.token_hex(32)  # or secrets.token_urlsafe(32)

# CRITICAL: hash encoding MUST match what the app's validator uses.
# Trilium uses SHA-256 base64 (NOT hex):
token_hash = hashlib.sha256(raw_token.encode()).digest()
import base64; token_hash_b64 = base64.b64encode(token_hash).decode()

# Insert with the correct hash
db.execute("INSERT INTO etapi_tokens (...) VALUES (?, ?, ...)", 
           (token_id, name, token_hash_b64, now, now))
db.commit()
print(f"Auth token: {raw_token}")
```

**Always check the validator source** before injecting. Look for `createHash("sha256").update(...).digest("base64")` vs `.digest("hex")`. They are NOT interchangeable.

## Architecture

```
Hermes Agent ──stdio──► MCP Server (raw mcp SDK) ──HTTP──► Local App
```

The MCP server is a thin Python bridge: it receives JSON-RPC from Hermes on stdio and forwards requests as HTTP calls to the app. This keeps Hermes's MCP client working with stdio transport while the app uses whatever HTTP protocol it has.

## Template

```python
#!/usr/bin/env python3
import os, sys, json, asyncio, logging, urllib.request, urllib.error
from typing import Any
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult

API_URL = os.environ.get("MYAPP_URL", "http://localhost:8080/api")
API_TOKEN = os.environ.get("MYAPP_TOKEN", "")
if not API_TOKEN:
    logging.error("MYAPP_TOKEN required"); sys.exit(1)

HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_TOKEN}"}

def _call(method: str, path: str, data: dict = None) -> Any:
    url = f"{API_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Cannot reach {url}: {e.reason}")

TOOLS = [
    Tool(name="myapp_health", description="Check connectivity",
         inputSchema={"type": "object", "properties": {}}),
]

server = Server("myapp")

@server.list_tools() async def list() -> list[Tool]: return TOOLS

@server.call_tool()
async def call(name: str, args: dict) -> CallToolResult:
    try:
        result = _call("GET", "/health")
        return CallToolResult(content=[TextContent(type="text",
            text=json.dumps(result, indent=2, default=str))])
    except Exception as e:
        return CallToolResult(isError=True,
            content=[TextContent(type="text", text=str(e))])

async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, InitializationOptions(
            server_name="myapp", server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=NotificationOptions(),
                experimental_capabilities={})))

if __name__ == "__main__": asyncio.run(main())
```

## Design Rules

### Must Use Raw `mcp` SDK, Not `fastmcp`

`fastmcp` 3.4.x has protocol-level incompatibilities:
- Constructor rejects `description` kwarg (`TypeError: FastMCP() got unexpected keyword argument(s): 'description'`)
- Handshake ordering breaks with `mcp>=1.0` clients (`Received request before initialization was complete`)

**Fix:** Use `mcp.server.Server` directly with `@server.list_tools()` and `@server.call_tool()` decorators. Works reliably with `mcp>=1.0,<1.3`.

### Graceful Degradation

If the target app isn't running, tools should return error messages, not crash Hermes. Wrap every HTTP call in try/except and return `CallToolResult(isError=True, ...)`.

### Env Vars for Config

URL, token, and any port go in env vars (passed via Hermes config `env:` block). Never hardcode. The `mcp_servers` config entry passes these cleanly:

```yaml
mcp_servers:
  myapp:
    command: python
    args: ["<abs-path>/server.py"]
    env:
      MYAPP_TOKEN: ${MYAPP_TOKEN}
      MYAPP_URL: http://localhost:8080
    timeout: 30
```

Add tokens to `~/.hermes/.env`. Restart Hermes after config changes.

### No `workdir` Support

MCP servers spawn without a configurable working directory. If your server needs a specific cwd (e.g. relative DB path), call `os.chdir()` at the top of `main()` using an absolute path or an env var.

## Config Wiring

Add to the profile's `config.yaml` under `mcp_servers:`:

```yaml
mcp_servers:
  myapp:
    command: python
    args: ["C:\\path\\to\\mcp_myapp_server.py"]
    env:
      MYAPP_TOKEN: ${MYAPP_TOKEN}
    timeout: 30
```

The args path must be absolute — Hermes may spawn the subprocess from any working directory.

## Testing Standalone

```python
import asyncio
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import ClientSession

async def test():
    params = StdioServerParameters(
        command="python", args=["/path/to/server.py"],
        env={"MYAPP_TOKEN": "test"})
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            t = await s.list_tools()
            print(f"{len(t.tools)} tools:", [x.name for x in t.tools])

asyncio.run(test())
```

## Pitfalls

- **fastmcp `description` kwarg** — removed in 3.4.x. Use raw `mcp` SDK.
- **Tool naming** — Hermes prefixes tools as `mcp_{server_name}_{tool_name}`. Keep names short.
- **Connection timeout** — If the app starts slowly, raise `timeout` in config (default 120s in Hermes, 30s in the template above).
- **Auth format** — Some apps want `Bearer <token>`, others want bare token in `Authorization`. Check the app's docs.
- **JSON vs raw body** — Some endpoints (Trilium note content) use raw text/html body, not JSON. The `_call()` function in the template sends JSON; add a `_call_raw()` variant when needed.
- **Hash encoding mismatch** — When injecting tokens into SQLite-backed apps, the hash encoding (hex vs base64) must match what the validator uses. Trilium uses SHA-256 base64. A hex hash when base64 is expected causes auth to silently fail.
- **Docker port 8080 occupied** — Docker Desktop's backend often binds port 8080 (PID 37600 = com.docker.backend.exe). Map other services to 8090+ to avoid conflict.
- **Windows YAML backslash trap** — Backslashes inside double-quoted YAML strings trigger escape sequence parsing. `"C:\Users\..."` fails because `\U` is seen as a Unicode escape. Fix: use forward slashes (`C:/Users/...`) which work on Windows, or escape each backslash (`C:\\Users\\...`). The YAML spec treats forward slashes identically to backslashes on Windows paths.

## Related

- [building-mcp-servers](../building-mcp-servers/) — broader MCP server lifecycle (from scratch, testing, discovery)
- [native-mcp](../native-mcp/) — Hermes MCP client config options
