---
name: maintain
description: GBrain-inspired maintenance for Codex. Use when the user wants a health check, consistency audit, stale-doc sweep, or package cleanup pass.
---

# Maintain

Use this skill when the user wants a maintenance pass over the repo, docs, trackers, or saved reports.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain runs health checks against a brain database, backlinks, and citation-bearing pages. In this repo, the closest equivalents are:

- registry and docs consistency
- missing or stale skill artifacts
- report/task file drift
- structural validation and targeted audits

## Workflow

1. Run the package checks first:
   - `python3 scripts/validate_repo.py`
   - `python3 -m unittest discover -s tests`
2. Inspect the relevant layer:
   - registries and docs
   - task or report files
   - skills and supporting references
3. Identify concrete issues:
   - stale docs
   - missing files
   - inconsistent paths or naming
   - uncategorized or duplicated reports
4. Fix what is safe and explicit.
5. Save or summarize a maintenance report when helpful.

## Current Upstream Coverage

Audit stale pages, orphans, dead links, missing backlinks, filing violations, citation debt, tag consistency, graph density, embedding freshness when applicable, schema health, storage health, and unresolved threads. Support a manual pass and an autonomous target-score loop, but never bulk-fix private brain content without a scoped plan and validation rerun.

## Guardrails

- Do not delete content without clear justification.
- Prefer specific fixes over vague "health check passed" language.
- Read before rewriting when a file is non-trivial.
