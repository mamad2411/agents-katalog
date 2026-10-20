---
applyTo: "**/wara_checks.yaml"
---

# WARA Checks Conventions

## Check ID Format

Use pillar prefix + sequential 3-digit number:

| Prefix | Pillar |
|--------|--------|
| `REL-` | Reliability |
| `SEC-` | Security |
| `COS-` | Cost Optimization |
| `OPE-` | Operational Excellence |
| `PER-` | Performance Efficiency |

## Required Fields

Every check must have: `id`, `title`, `pillar`, `caf_area`, `alz_area`,
`severity`, `scope`, `query_type`, `query`, `match`, `recommendation`.

## Severity Assignment

- **Critical**: Security baseline violation, data loss risk, compliance blocker
- **High**: WAF/CAF misalignment with operational impact
- **Medium**: Best practice gap, moderate risk
- **Low**: Minor improvement, informational

## KQL Query Rules

- Always `project` only the fields needed (no `select *`)
- Always include `id`, `name`, `resourceGroup`, `subscriptionId` for traceability
- Use `=~` for case-insensitive type comparisons
- Limit results to avoid Resource Graph throttling

## Match Types

- `any` — Finding is raised when query returns results (non-compliant resources exist)
- `empty` — Finding is raised when query returns no results (expected resource missing)
- `custom` — Requires `evaluation` field pointing to a `WaraEngine` method name

## Confidence Guidelines

- **High**: Deterministic query, no false positives expected
- **Medium**: May need manual review, context-dependent
- **Low**: Heuristic, informational signal

## Adding a New Check

1. Add entry to `src/config/wara_checks.yaml`
2. If `query_type: custom`, add evaluation method to `src/tools/wara_engine.py`
3. No other code changes needed — engine loads checks dynamically
