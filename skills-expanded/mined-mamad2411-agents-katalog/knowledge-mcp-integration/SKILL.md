---
name: knowledge-mcp-integration
version: 1.1.0
description: Build, diagnose, and integrate knowledge management MCP servers into Hermes Agent — covering file-based servers, HTTP API servers, bidirectional linking, structured hierarchies, and token auth debugging.
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [knowledge-management, mcp, logseq, trilium, wiki, file-based, linking, knowledge-graph, hermes]
    triggers: [integrate knowledge tools, build MCP server, connect logseq trilium wiki to hermes, knowledge management MCP, file-based MCP server, knowledge graph integration, knowledge base integration, wiki integration]
    related_skills: [native-mcp, building-mcp-servers]
---

# Knowledge MCP Integration — Build & Wire Knowledge Tools into Hermes

This skill covers building, diagnosing, and integrating knowledge-management
MCP servers into Hermes Agent. Knowledge management tools store linked,
structured, or hierarchical information — wikis, note-taking apps, knowledge
bases, personal knowledge graphs.

## Two Architectures for Knowledge MCP Servers

Knowledge tools come in two flavors, and each maps to a different MCP server
architecture:

### 1. File-Based MCP Server (No HTTP API Needed)

For tools that store data as local files (Logseq, Obsidian, Zettlr, Foam,
Dendron). The MCP server reads/writes files directly — no running app, no
ports, no Docker.

**When to choose:**
- Data is stored as plain-text files (markdown, JSON, YAML)
- You want zero infrastructure dependencies
- Data must survive restarts without Docker
- You need instant response times (local filesystem)

**Trade-offs:**
- File locking needed for multi-client access
- No concurrent write safety without explicit locking
- Can't query via SQL or HTTP

**Implementation pattern:**

```python
# Core structure for a file-based knowledge MCP server
from mcp.server import Server, NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, CallToolResult
from pathlib import Path
import os, json, re

DATA_DIR = Path(os.environ["KNOWLEDGE_DIR"])
TOOLS = [...]  # Define your tools

def _read(name): ...
def _write(name, data): ...
def _search(query): ...
def _graph(): ...

server = Server("knowledge-mcp")
@server.list_tools() async def lt(): return TOOLS
@server.call_tool() async def ct(n, a): return await handle(n, a)

async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, InitializationOptions(...))
```

For a complete reference implementation with 17 tools (pages, blocks,
journals, wikilinks, backlinks, graph, search), see the Logseq File MCP
server at `mcp_logseq_file_server.py` which reads/writes standard Logseq
markdown files.

### 2. HTTP API MCP Server (For Running Services)

For tools that expose a REST/HTTP API (Trilium, Joplin Server, SiYuan,
Confluence, Notion API). The MCP server wraps API calls.

**When to choose:**
- The tool has a well-documented REST API or SDK
- You need server-side features (search indexing, scripting, user auth)
- Multiple clients need concurrent access
- You already run the tool as a Docker container or service

**Trade-offs:**
- Requires the service to be running
- Network latency on every call
- API version compatibility over time
- Token/key management

**Auth debugging pitfall — hash encoding mismatch:**

A common failure when connecting to token-authenticated APIs is the server
rejecting a known-good token. The root cause is often **hash encoding
mismatch**:

```python
# TRILIUM stores token hashes as SHA-256 BASE64:
hash = hashlib.sha256(token.encode()).digest("base64")
# "BXncXOZMX7g+VTh2v47L2lRpAhPj+LCNK7UjTd0AkS4="

# WRONG assumption — hex encoding:
hash = hashlib.sha256(token.encode()).hexdigest()
# "0579dc5ce...f74024b92e"  ← won't match
```

**Debugging pattern when auth fails:**

1. Read the server's source code to find the exact hash function
2. Check: is the hash stored in `hex` or `base64` format?
3. Check: is the token format `id_token` (with underscore separator) or raw?
4. Check: does the Authorization header need `Bearer ` prefix?
5. Test with curl first, then wrap in MCP server

For Trilium specifically:
- Auth header: `Authorization: Bearer <raw_token>` or `Authorization: <raw_token>`
- Token stored as SHA-256 base64 hash in `etapi_tokens` table
- Token format for API-created tokens: `<etapiTokenId>_<raw>`
- For manually injected tokens: raw token with matching hash in DB

## Knowledge Tier Architecture

When integrating multiple knowledge tools, tier them by access speed and
structure:

```
Tier 1: Memory (fastest, key-value)
  → User preferences, environment facts, durable conventions
  → Sub-millisecond, survives everything
  → Backend: built-in, Honcho, Mem0

Tier 2: File-Based MCP (fast, file-based blocks/links)
  → Free-form linked reasoning, session notes, journals
  → [[wikilinks]] for cross-referencing concepts
  → Block-level granularity, graph queries
  → No infrastructure needed

Tier 3: Structured MCP (server-based, attributes/relations)
  → Hierarchical project docs, SOPs, architecture records
  → Full CRUD, search, scripting
  → Requires running service (Docker, desktop app)
```

Data flow: Agent Decision → File MCP (linked reasoning) → Structured MCP
(organized storage) → Memory (fact extraction for persistence).

## Config.yml Wiring

Both architectures wire the same way — the key difference is how the
server accesses its data:

```yaml
mcp_servers:
  # File-based — reads/writes from a directory
  logseq:
    command: python
    args: ["path/to/mcp_server.py"]
    env:
      KNOWLEDGE_DIR: C:/Users/Me/.logseq/my-graph
    timeout: 30

  # HTTP API — connects to a running service
  trilium:
    command: python
    args: ["path/to/mcp_etapi_server.py"]
    env:
      API_TOKEN: ${SECRET_TOKEN}
      API_URL: http://localhost:8090
    timeout: 30
```

## Verification Checklist

- [ ] File-based: directory exists and is readable/writable
- [ ] File-based: test with a quick read/write cycle via the MCP tools
- [ ] HTTP API: service is running (`docker ps`, `curl <url>/health`)
- [ ] HTTP API: token auth works (`curl -H "Authorization: Bearer $TOKEN" <url>`)
- [ ] All tools list correctly via `mcp` client
- [ ] At least one read tool and one write tool work end-to-end
- [ ] Graph/backlink features return non-empty results when data is linked
- [ ] Config is wired in the correct profile's config.yaml
- [ ] Restart Hermes to pick up the new MCP server

## Pitfalls

- **File-based: encoding mismatch** — Always use UTF-8. Logseq, Obsidian,
  and most markdown-based tools expect UTF-8 for all files.
- **File-based: write atomicity** — File-based servers read-then-write.
  Single-agent use (Hermes alone) is fine. Multi-agent = add file locking.
- **File-based: Unicode filenames** — Logseq normalizes aggressively.
  Unicode characters in page titles may produce unexpected filenames. Test
  the slug function before relying on path resolution.
- **HTTP API: port conflicts** — Docker `-p 8080:8080` fails if another
  process has the host port. Use a different host port (`8090:8080`) or
  find the conflict with `netstat -ano | grep LISTENING | grep <port>`.
- **HTTP API: token auth hash encoding** — SHA-256 can be base64 or hex.
  Read the server source to confirm which. Mismatch = silent auth failure.
- **HTTP API: Docker restart policy** — Always set `--restart unless-stopped`
  so the service survives reboots: `docker update --restart unless-stopped <container>`.
- **Knowledge tier creep** — Don't store everything in all three tiers.
  Tier 2 is for linked reasoning (journals, connections, thoughts). Tier 3
  is for structured canonical records. Memory is for durable facts that
  never change. Mixing tiers creates stale duplicates.
