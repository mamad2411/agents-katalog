---
description: Run every test that works without credentials (offline Gmail, MCP protocol, docs links, installer syntax) and report the results
---

Run these from the repository root and report pass/fail counts for each. Stop and diagnose on the first failure; do not edit tests to make them pass unless the test itself is wrong.

```bash
uv run --with fastapi --with aiohttp --with python-dotenv --with httpx python tests/protocol.py
uv run --with fastapi --with aiohttp --with python-dotenv --with httpx python tests/dashboard.py
uv run --with fastapi --with aiohttp --with python-dotenv python tests/gmail_offline.py
uv run --with fastapi --with aiohttp --with python-dotenv python tests/discord_offline.py
python tests/claude_config.py
python scripts/check_claude_config.py
uv run --with aiohttp python scripts/gen_tools_doc.py --check
python tests/check_docs.py
node --check scripts/capes.mjs && node --check dashboard/app.js
uvx ruff check . && uvx ruff format --check .
```

Optional, only if the user asks and provides a disposable Discord test server (never a real community server):

```bash
# terminal 1: MCP_API_KEY=localtestkey DISCORD_BOT_TOKEN=... uv run --with fastapi --with aiohttp --with python-dotenv --with uvicorn python api/index.py
GUILD=<test-server-id> MODE=read python tests/discord_e2e.py     # read-only, safe anywhere
GUILD=<test-server-id> MODE=full python tests/discord_e2e.py     # posts and deletes things: test server only
```

Live Gmail is verified by the maintainer with a real app password by calling `gmail_list_labels`, `gmail_search`, and a send-to-self, never by committing message content.
