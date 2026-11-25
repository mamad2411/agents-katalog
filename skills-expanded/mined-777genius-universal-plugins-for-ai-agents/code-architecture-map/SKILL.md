---
name: code-architecture-map
description: Build a compact architecture map of a repository using CGC, Semble, rg, and source reads.
execution_mode: docs_only
supported_agents:
  - codex
  - claude
---

# Code Architecture Map

## What it does

Creates a compact architecture map with entry points, core domains, adapters, risky files, verification points, and recommended next reads.

## When to use

Use this when entering a large repo, reviewing architecture, finding high-risk modules, or planning a multi-file change.

## How to run

1. Read project instructions first: `AGENTS.md`, `CLAUDE.md`, `README.md`, and package manifests.
2. Use `rg --files` to understand languages and major folders.
3. Use CGC stats and complexity to identify hotspots.
4. Use Semble for semantic entry points by feature or domain.
5. Read only the files needed to confirm the map.
6. Produce a short architecture summary with risks and next actions.

Commands:

```bash
rg --files | sed -n '1,160p'
cgc stats . --context "$(basename "$PWD")"
cgc analyze complexity --limit 25 --context "$(basename "$PWD")"
cgc report --output /tmp/CGC_REPORT.md --context "$(basename "$PWD")"
uvx --from semble==0.2.0 semble search -k 10 "main application flow" .
```

## Constraints

- Do not paste a giant file tree.
- Do not claim graph output is complete until source files confirm it.
- Prefer a useful map over inventory noise.
- Keep output focused on decisions, risks, and next reads.
