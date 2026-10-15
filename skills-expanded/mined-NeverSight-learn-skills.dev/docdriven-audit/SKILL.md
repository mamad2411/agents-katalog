---
name: docdriven-audit
description: Use to audit a DocDriven project for stale docs, missing routes, duplicate truth, invalid context maps, oversized files, tmp content that should be promoted, and weak validation evidence.
---

# DocDriven Audit

Use this skill to check documentation drift and maintainability.

## Required Workflow

1. Read the repo-local `project-docdriven` skill if present.
2. Read `Docs/agent/manifest.json`.
3. Load route shards listed by the manifest.
4. Run deterministic checks with `scripts/audit-docdriven.mjs` when possible.
5. If no repo-local audit entrypoint exists, use the installed global audit
   script as a fallback and report the missing local entrypoint as a P3
   reproducibility issue.
6. Inspect reported gaps manually.
7. Report findings by severity.
8. Update docs only when asked.

Audit checks the route graph, referenced docs, referenced code areas, validation
evidence, placeholder text, oversized shards, orphan knowledge docs, tmp
content, context-map drift, weak architecture contracts, undocumented structure
signals, missing configuration-pattern documentation, and missing
reuse/composition documentation for reusable project primitives.

The audit should remain project-aware. Before judging structure, consider the
project type, size, maturity, direction, and risk profile. Small projects should
not be forced into heavyweight routing, but large projects need reproducible
checks, clear ownership, narrow route shards, and stronger evidence that docs
match code.

A DocDriven project should have a stable local audit command. Prefer a thin
`scripts/audit-docdriven.mjs` wrapper that invokes the installed DocDriven audit
implementation and fails with a clear install or upgrade hint when it cannot be
found. For Node projects, prefer documenting or adding a package script such as
`docs:audit`.

## References

- Read `../_shared/audit-checklist.md`.
- Read `../_shared/agent-operating-contract.md`.
