---
name: protocolbox
description: >
  Standard Library of verified tools for AI Agents.
  Tools: scrape(url), heal_json(str).
---

# ProtocolBox

## Installation

```bash
pip install protocolbox
```

## Usage

Start the MCP server:

```bash
protocolbox start
```

Or with uv:

```bash
uv run protocolbox start
```

## Available Tools

- **scrape(url: str) -> str** — Fetch a web page and return clean Markdown.
- **heal_json(broken_json: str) -> dict** — Fix malformed JSON from LLM output.
