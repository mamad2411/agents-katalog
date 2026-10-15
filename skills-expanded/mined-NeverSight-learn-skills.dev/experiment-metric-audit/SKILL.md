---
name: experiment-metric-audit
description: Vendor-neutral skill for auditing experiment metrics definitions for common analytics pitfalls and inconsistencies.
---

## When to invoke
- You have an A/B test plan with metric definitions captured in JSON.
- You want to validate that metric formulas, unit of analysis, and guardrails are internally consistent.
- You need vendor-neutral checks before implementing metrics in any analytics stack.

## Inputs needed
- JSON file describing an experiment and its metrics (primary/secondary/guardrail).

## Workflow
1. Validate schema (experiment name, variants, metrics list).
2. Check each metric for:
   - missing unit of analysis (user, session, order)
   - missing time window
   - unclear numerator/denominator for ratio metrics
   - guardrail metrics present (e.g., error rate) when risky changes are described
3. Detect common inconsistencies:
   - metrics mixing units (user-level denominator with event-level numerator)
   - duplicate metric names
4. Emit a structured audit report with actionable recommendations.

## Output format
- JSON report with findings and a summary score.
- Human-readable markdown printed to stdout.

## Guardrails
- Do not claim statistical validity; this is a definition audit only.
- Treat output as a checklist; analyst review required.

## Reference code
- `experiment_metric_audit.py`
