---
name: cloud-cost-tag-coverage-auditor
description: Audit cloud resource export data for missing or invalid cost allocation tags and output a vendor-neutral remediation plan.
---

## When to invoke
- You need cost allocation hygiene across teams/environments.
- You have a resource export (CSV) and want to quantify tag coverage.
- You want a prioritized remediation plan (which owners/projects to fix first).

## Inputs needed
- A CSV with a row per resource, containing:
  - `resource_id`
  - `service`
  - `cost_monthly`
  - tag columns, e.g. `tag_owner`, `tag_cost_center`, `tag_env`
- A JSON policy file listing required tags and allowed values (optional).

## Workflow
1. Load CSV and infer tag columns (prefix `tag_`).
2. Validate required tags:
   - present and non-empty
   - optional allowed-values checks from policy
3. Compute:
   - overall tag coverage rate
   - cost-weighted coverage rate
   - top missing tags by cost impact
4. Build a remediation plan:
   - prioritize by cost impact
   - group by service and owner tag (if available)
5. Emit JSON report.

## Output format
JSON to stdout:
- `coverage`: overall and cost-weighted
- `missing_by_tag`: counts and cost impact
- `top_resources_to_fix`
- `remediation_plan`

## Guardrails
- Vendor-neutral: works with generic CSV exports and tag conventions.
- Do not assume a specific cloud provider.

## Reference code
- `cloud_cost_tag_coverage_auditor.py`
