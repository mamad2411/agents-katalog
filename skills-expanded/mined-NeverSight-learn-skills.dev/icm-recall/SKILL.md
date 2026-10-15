---
name: icm-recall
description: Searches ICM persistent memory from Codex. Use when the user invokes `icm-recall`, asks to recall or search ICM memory, asks what ICM remembers, or provides a query that should be looked up in long-term memory.
---

# ICM Recall

Search ICM for the user's query and report only relevant memories concisely.
Prefer the ICM MCP recall tool. If MCP is unavailable, use the local ICM CLI
through `rtk run`:

```bash
rtk run 'icm recall "<query>"'
```
