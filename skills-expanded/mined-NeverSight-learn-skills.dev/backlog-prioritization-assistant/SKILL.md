---
name: backlog-prioritization-assistant
description: Vendor-neutral skill to prioritize a backlog using configurable scoring (RICE/WSJF-style) and produce a ranked list with rationale.
---

## When to invoke
- You have a backlog of initiatives and want a repeatable prioritization with transparent scoring.
- You need to generate a "next up" list for planning from a CSV export.

## Inputs needed
- `--input` path to a CSV with one row per item.
  - Required columns: `id`, `title`, `impact`, `effort`
  - Optional columns: `reach`, `confidence`, `cost_of_delay`, `job_size`
- `--method` one of: `rice`, `wsjf`, `simple`.

## Workflow
1. Validate required columns and parse numeric fields.
2. Compute a score per item:
   - RICE: \(\text{reach} \times \text{impact} \times \text{confidence} / \max(\text{effort},\epsilon)\)
   - WSJF: \(\text{cost_of_delay} / \max(\text{job_size},\epsilon)\)
   - Simple: \(\text{impact} / \max(\text{effort},\epsilon)\)
3. Apply tie-breakers (higher impact, lower effort).
4. Emit a ranked JSON report with per-item rationale.

## Output format
- JSON written to `--output`:
  - `items`: ranked list with `score` and `explanations`
  - `summary`: method and any validation warnings

## Guardrails
- Do not claim the ranking is "correct"; treat as decision support.
- Never fabricate missing fields; default optional fields conservatively.

## Reference code
- `backlog_prioritization_assistant.py` implements CSV parsing + scoring (stdlib-only).
