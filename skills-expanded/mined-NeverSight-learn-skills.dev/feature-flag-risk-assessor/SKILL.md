---
name: feature-flag-risk-assessor
description: Vendor-neutral skill to assess risk in feature-flag configurations (stale flags, kill-switch coverage, conflicting rules) and produce actionable recommendations.
---

## When to invoke
- You have a feature-flag export (JSON) and want to identify operational and release risks.
- You want to standardize flag hygiene checks during releases.

## Inputs needed
- `--input` path to a JSON file containing feature flags.
  - Expected shape: `{ "flags": [ {"key": "...", "created_at": "YYYY-MM-DD", "updated_at": "YYYY-MM-DD", "enabled": true/false, "rules": [...] } ] }`

## Workflow
1. Validate the flag schema and required fields.
2. Compute risk signals:
   - stale flags (no updates beyond threshold)
   - enabled flags older than threshold
   - flags without a documented owner
   - rule conflicts (duplicate segments with different rollouts)
   - missing kill-switch (no global off / override rule)
3. Emit a JSON report with per-flag risk score and suggested actions.

## Output format
- JSON written to `--output`:
  - `summary`: counts by risk type
  - `flags`: per-flag findings + `risk_score` (0-100)

## Guardrails
- Do not attempt to evaluate user targeting deterministically; only analyze configuration structure.
- Prefer explainable heuristics over opaque scoring.

## Reference code
- `feature_flag_risk_assessor.py` implements a heuristic risk analyzer (stdlib-only).
