---
name: kpi-definition-consistency-checker
description: Vendor-neutral skill to check a KPI dictionary for conflicting definitions, grain mismatches, and missing ownership.
---

## When to invoke
- You maintain a metrics catalog and want consistency across teams.
- You suspect KPI definitions drifted (different denominators, time windows, or grains).

## Inputs needed
- KPI dictionary JSON: `kpis[]` where each KPI has:
  - `name`, `description`, `numerator`, `denominator`, `grain`, `window`, `owner`, `source_tables[]`

## Workflow
1. Normalize names and detect near-duplicates.
2. Validate required fields and flag missing owners/windows/grain.
3. Detect potential conflicts:
   - Same KPI name but different numerator/denominator
   - Different grain (user vs account vs event)
   - Window mismatch (7d vs 30d)
4. Emit a report with issues and a suggested canonicalization list.

## Output format
- JSON report:
  - `summary`
  - `issues[]` (severity, kpi, problem, details)
  - `duplicate_groups[]`

## Guardrails
- Heuristic checks only; do not claim semantic equivalence.
- Do not query databases; rely solely on provided dictionary.

## Reference code
- `kpi_definition_consistency_checker.py` reads KPI JSON and outputs a consistency report.
