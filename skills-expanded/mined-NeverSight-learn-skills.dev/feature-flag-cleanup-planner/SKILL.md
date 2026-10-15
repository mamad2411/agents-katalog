---
name: feature-flag-cleanup-planner
description: Vendor-neutral skill to prioritize feature flags for cleanup using simple heuristics and produce a deprecation plan.
---

## When to invoke
- You have a list of feature flags and want to reduce config debt safely.
- You want to identify stale flags, flags permanently enabled, or flags with no recent evaluation.

## Inputs needed
- `--flags`: JSON file containing an array of flags with metadata.
- Fields expected per flag (best-effort):
  - `key` (string)
  - `created_at` (ISO date)
  - `last_evaluated_at` (ISO date, optional)
  - `owner` (string, optional)
  - `default` (`on|off`)
  - `environments`: object like `{ "prod": {"state":"on|off", "percentage":0-100} }`
  - `notes` (string, optional)

## Workflow
1. Parse and normalize the flag inventory.
2. Compute heuristics per flag:
   - age in days
   - days since last evaluation
   - permanently on/off in prod
   - risky rollout (prod percentage between 1 and 99)
3. Assign a recommended action:
   - `remove` (stale + permanently on/off)
   - `migrate_to_config` (long-lived flag acting like config)
   - `keep` (recently evaluated or in active rollout)
4. Output a ranked plan with suggested steps and a checklist.

## Output format
JSON:
- `summary`
- `plan`: list of `{key, score, recommended_action, rationale, checklist}` sorted by score descending

## Guardrails
- Never recommend removing flags in active rollout (1–99% in prod).
- Prefer `migrate_to_config` if a flag is old and permanently on but likely used as a kill-switch.
- Output must be explainable and deterministic.

## Reference code
`plan_cleanup.py`
