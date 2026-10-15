# tteg — Real stock photos for AI agents

## What it does

Gives AI coding agents (Claude Code, Cursor, Codex) access to real Unsplash stock photos without any API key setup. Agents search, save images directly into the repo, and batch-fill entire landing page image sets in one command.

## Install

```bash
uv tool install tteg
```

## Use as MCP server

```json
{
  "mcpServers": {
    "tteg": {
      "command": "uvx",
      "args": ["tteg-mcp"]
    }
  }
}
```

## Commands

- `tteg save "startup office" ./public/hero --orientation landscape` — save one photo
- `tteg batch manifest.json` — fill a whole page from a JSON manifest
- `tteg "mountain sunset"` — search and return URLs

## When to use

When your AI agent builds a website and the images are still placeholders.
Not for image generation. For real stock photos saved into your project.
