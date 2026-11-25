---
name: run-pinrag-unit-tests
description: >-
  Runs the full PinRAG pytest suite with uv after loading API keys from ~/.cursor/mcp.json
  (e.g. pinrag-dev). Use when the user wants all tests, pytest, or CI locally for pinrag.
---

# Run PinRAG tests

From the **pinrag repo root** (directory with `pyproject.toml`), run the **`eval` … `pytest` line below** (one chained command). It reads **`~/.cursor/mcp.json`** → **`mcpServers.pinrag-dev.env`** (OpenAI, OpenRouter, Anthropic, etc.—not “OpenAPI”). Use another `mcpServers` key: set it on the same line (see `export` below).

**Secrets:** never paste `mcp.json` values into chat.

```bash
export PINRAG_MCP_JSON_KEY="${PINRAG_MCP_JSON_KEY:-pinrag-dev}"; eval "$(python3 -c "import json, pathlib, shlex, os; k=os.environ[\"PINRAG_MCP_JSON_KEY\"]; e=json.loads((pathlib.Path.home()/\".cursor/mcp.json\").read_text()).get(\"mcpServers\",{}).get(k,{}).get(\"env\")or{}; [print(\"export \"+n+\"=\"+shlex.quote(str(e[n]))) for n in sorted(e)]")" && export PINRAG_LLM_PROVIDER="${PINRAG_LLM_PROVIDER_TEST:-openai}" PINRAG_LLM_MODEL="${PINRAG_LLM_MODEL_TEST:-gpt-4o-mini}" && uv sync --all-extras && uv run pytest
```

The **`PINRAG_LLM_*`** exports avoid failures when `mcp.json` pins OpenRouter but integration tests (e.g. multi-query) still hit OpenAI chat with a non-OpenAI model id. Drop them if your MCP entry already uses **`PINRAG_LLM_PROVIDER=openai`** with a real OpenAI chat model.

**Fast run** (no integration / PyPI MCP):  
`uv sync --extra dev && uv run pytest -m "not integration and not pypi_mcp"`
