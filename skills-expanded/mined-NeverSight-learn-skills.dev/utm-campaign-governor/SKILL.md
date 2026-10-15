---
name: utm-campaign-governor
description: Enforces vendor-neutral UTM naming conventions by validating marketing links and generating a normalized, policy-compliant output.
---

## When to invoke
- You manage marketing campaigns and need consistent UTM tags across teams.
- You want to validate a batch of URLs against a naming policy and produce corrected URLs.

## Inputs needed
- `--input`: CSV with a `url` column.
- Optional: `--policy`: JSON policy file (allowed sources/mediums, required params, casing rules).
- Optional: `--out`: Path to write results CSV.

## Workflow
1. Load URLs.
2. Parse query parameters.
3. Validate required UTM params (`utm_source`, `utm_medium`, `utm_campaign`).
4. Validate allowed values (if provided) and casing rules.
5. Produce:
   - `status`: ok / fixed / invalid
   - `issues`: semicolon-separated
   - `normalized_url`: URL with normalized UTMs (when possible)

## Output format
CSV with columns:
- `url`
- `status`
- `issues`
- `normalized_url`

## Guardrails
- Never change the base URL path or non-UTM query params.
- Do not guess missing required params; mark as invalid.
- Keep the skill vendor-neutral (no platform-specific assumptions).

## Reference code
Use `utm_campaign_governor.py`.
