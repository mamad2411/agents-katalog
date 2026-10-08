---
name: consistency-audit
description: Check census data for inconsistencies or arithmetic errors. Use for "anything inconsistent?", "check the math", "audit".
---

# Consistency Audit recipe

1. Pull the named tables using `query_tables`.
2. Use `execute_python` to run pandas checks.
   - Checks to run: rural + urban ≈ total, percentages ∈ [0, 100], sum of categories ≈ 100, 2001 → 2011 direction sanity check.
3. Report each violation found with citations. If no violations are found, report that as a valid, citable answer.
   - Reply with `kind="text"`: `answer_md` = summary of findings, and claims citing the sources.

## Gotchas
- Minor rounding errors (e.g., 99.9% instead of 100%) are acceptable and should be noted but not treated as critical failures unless they exceed 0.5%.
- Sex ratio is females per 1000 males, not a percentage.
