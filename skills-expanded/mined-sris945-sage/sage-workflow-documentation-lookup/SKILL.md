---
name: sage-workflow-documentation-lookup
description: SAGE — prefer current official docs and project sources over stale memory when APIs or libraries matter.
---

# SAGE workflow — Documentation lookup

## Purpose

When the task depends on **accurate library or framework behavior** (versions, APIs, config), **do not** rely on training memory alone. Use **current** sources: official docs, package changelogs, or **MCP / browser tools** if available in the environment.

## When to activate

- “How do I configure X?” for a named framework.
- Code that must match a specific API surface.
- Version-sensitive behavior (language minors, major framework releases).

## Workflow

1. **Identify** the library and version from the repo (`package.json`, `pyproject.toml`, lockfiles).
2. **Fetch** authoritative text — docs site, release notes, or a docs MCP if configured.
3. **Answer** from that evidence; cite version when it matters.
4. **Limit** repeated doc fetches — batch questions; avoid thrashing the same page.

## SAGE-specific

- Read **project** conventions first (`README`, `CONTRIBUTING`, `.sage/**`, `docs/`).
- If **SAGE** exposes no doc MCP, use **web fetch** or **local files** under the workspace.

## Security

- Never paste secrets into doc search queries or logs. Redact tokens.
