---
name: priorities
description: Use when the user wants a prioritized content roadmap or asks what to work on next. This skill can run a quick-win-only path or a comprehensive multi-report path and summarizes the outputs.
---

# Priorities

Generate a content roadmap from the repository's research scripts.

## Quick Mode

```bash
.venv/bin/python scripts/run_priorities.py --mode quick
```

## Comprehensive Mode

```bash
.venv/bin/python scripts/run_priorities.py --mode comprehensive
```

Skip competitor gaps if API cost or credentials are a concern:

```bash
.venv/bin/python scripts/run_priorities.py --mode comprehensive --skip-gaps
```

## What This Produces

- A summary file in `research/priorities-<date>.md`
- Underlying research reports such as:
  - `quick-wins`
  - `performance-matrix`
  - `topic-clusters`
  - `trending`
  - optionally `competitor-gaps`

## What Codex Should Do Next

- Promote the top 3 actions into concrete tasks
- Route existing URLs to `analyze-existing` or `rewrite`
- Route net-new opportunities to `research`, `article`, or `write`
