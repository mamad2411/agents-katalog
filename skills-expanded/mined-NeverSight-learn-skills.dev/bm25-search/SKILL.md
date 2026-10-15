---
name: bm25-search
description: >-
  BM25 full-text code search over the local repo (SQLite FTS5). Use when
  exploring a codebase, finding definitions/usages, or answering "where is X"
  questions. Prefer before broad glob/grep to reduce tokens. Slash: /bm25-search
license: MIT
compatibility: Requires Python 3.10+ with SQLite FTS5
---

# BM25 Search

Ranked fragments first, then targeted reads. No MCP. Zero pip deps.

## Script

`SCRIPT` = this skill's `scripts/bm25.py` (next to this SKILL.md).

```bash
python "$SCRIPT" init .                              # first time / schema upgrade
python "$SCRIPT" search "keywords" -k 5 --auto-index
python "$SCRIPT" search "createSession" --mode def -k 5
```

Windows: `python` or `py -3`. Index: `<repo>/.bm25/index.sqlite`.

## Workflow

1. **One search** with `--auto-index` (default output is compact `min` format).
2. Read only top **1–3** `path:start-end` ranges (never whole files).
3. Stop if answerable; else one refined search (`--mode def|use|doc`) — not grep loops.
4. Do not re-read a path:range already in context.
5. Exact symbol → one query is enough; skip multi-grep after a clear hit.

## Modes

| Flag | When |
|------|------|
| `--mode code` | default; drops test paths unless query says test |
| `--mode def` | find definitions |
| `--mode use` | find call sites |
| `--mode doc` | prefer docs/md |

## Output (`--fmt min` default)

```
3.1 src/auth/session.ts:40-70|export function createSession(
```

Flags: `-k 5`, `--snippet 80`, `--paths-only`, `--json`, `--fmt text`, `--auto-index`.

Exit: `0` hits · `1` none · `2` error / missing index.

## Token rules

- BM25 before exploratory glob/grep.
- Default **k=5**; raise only if needed.
- Never dump full files from search.
- Prefer fewer tool rounds over exhaustive exploration.
