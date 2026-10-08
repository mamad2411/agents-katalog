---
name: "observability-gap-review"
description: "Review a system for missing or weak logs, metrics, traces, request IDs, and operational diagnostics. Use when a user asks for observability review, production debugging readiness, telemetry gap analysis, or as part of $full-test-suite deep-audit work."
---

# Observability Gap Review

Find observability gaps that make incidents or regressions harder to detect and debug.

## Focus Areas

- missing request IDs, correlation IDs, or audit trails
- poor error logging or sensitive over-logging
- absent metrics or traces on critical paths
- silent failure or retry behavior with no operator visibility

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Severity rubric: `../_shared-project-ops/references/severity-rubric.md`
