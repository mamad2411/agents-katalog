---
name: datadog-search-evidence
description: Search Datadog logs, traces, metrics, events, and related telemetry for evidence tied to a service, request, trace, error, deployment, or incident. Use when an engineering investigation needs runtime evidence before drawing conclusions.
---

# Search Evidence

1. Read service observability metadata and resolve environment, service name, and time window.
2. Build the narrowest useful search using service, environment, request/trace IDs, error signatures, deployment version, and known dependency names.
3. Search independent telemetry sources in parallel when useful.
4. Preserve timestamps, correlation IDs, service/version tags, and relevant error context.
5. Expand the search window or dependency scope only when evidence requires it.
6. Separate observed evidence from inference.

## Output
- Search Scope
- Evidence Found
- Correlations
- Unknowns
- Recommended Next Skill
