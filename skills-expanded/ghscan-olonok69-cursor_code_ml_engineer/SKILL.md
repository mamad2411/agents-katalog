---
name: kg
description: >-
  History-first ticket knowledge-graph lookup. Use at session start or whenever
  orienting on a bug/area — before grepping data/changes/. Surfaces related
  prior tickets and danger zones from the graphify-built index (or STATUS fallback).
---

# kg — ticket knowledge graph query

## When to use

- Stage **1 Orient** of the methodology.
- User mentions a ticket id, symptom area, extractor, or “have we seen this before?”.
- Before broad reads under `data/changes/`.

## Procedure

1. If the repo has knowledge-graph scripts (often under `docs/knowledge-graph/` or `data/knowledge-graph/`), run the local query helper, e.g.:

```bash
# Adjust path to the real script in this repo
./docs/knowledge-graph/kg_query.sh "<ticket-or-topic>"
```

On Windows PowerShell, prefer the same script via `bash`/`wsl` if that is how the project runs it.

2. Read **only** the files/nodes the query says to read (related tickets + sharp-edge / danger zone).
3. Also check live state: `git branch -a`, `gh pr list` (status-first).
4. Summarize for the human: prior art, locked invariants, suggested base branch — **do not start coding**.

## Fallback (no graph)

If query tools/artifacts are missing:

1. Search `data/changes/STATUS.md` for the topic / symptom terms.
2. Open the newest matching `data/changes/<id>/<id>.md`.
3. Skim `data/changes/SHARP_EDGES.md`.
4. Use `git log --oneline -- <paths>` for file-overlap history.

State clearly that you used the fallback.

## Output format

```text
KG / history-first
- Query: …
- Related tickets: …
- Danger zones / sharp edges: …
- Live status (branch/PRs): …
- What to read next: …
- Recommendation: (base / constraints / whether to proceed to triage)
```
