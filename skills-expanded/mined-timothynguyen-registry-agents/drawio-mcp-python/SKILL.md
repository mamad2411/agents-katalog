---
name: drawio-mcp-python
version: 0.1.0
description: |
  Python FastMCP server for opening draw.io diagrams from XML, CSV, and Mermaid
  input. Use when users need diagram rendering, draw.io preview links, or a
  local MCP tool provider compatible with the Node drawio-mcp protocol.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [diagram-agent, swe, qa-agent]
mcp: drawio-mcp-python
trigger: drawio|draw.io|diagram|mermaid|mxGraphModel
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Draw.io MCP Python

Use this tool provider to open diagram content in draw.io through FastMCP.

## Setup

```bash
cd drawio-mcp-python
pip install -e .
drawio-mcp
```

## Tools

- `open_drawio_xml` opens draw.io XML or `mxGraphModel` content.
- `open_drawio_csv` opens draw.io CSV import data.
- `open_drawio_mermaid` opens Mermaid diagram syntax.

## Workflow

1. Validate diagram input locally before opening draw.io.
2. Prefer Mermaid or CSV for generated diagrams unless user already has XML.
3. Use lightbox mode for previews and editable mode only when user needs editing.
4. Keep generated diagram source in repo docs or artifacts when it is part of deliverable.
