---
description: Documentation governance rules
globs: docs/**
alwaysApply: false
---

# Documentation Governance

See `docs/reference/doc-governance.md` for full rules.

## Allowed paths under /docs

- tutorials/ — learning paths
- how-to/ — task guides
- reference/ — technical references, policies, indexes
- explanation/ — architecture rationale, governance
- adrs/ — architecture decision records
- runbooks/ — operational procedures

## Forbidden

- Do not create /reports, /docs/reports, or ad-hoc doc folders.
- Do not place evidence/artifacts in /docs. Use /artifacts.
- Do not duplicate prompt content in docs.
- Do not create marketing fluff or speculative feature docs.

## ADRs

Enterprise-namespaced: `VE-PLAT-ADR-NNNN`.
Every ADR must be registered in `docs/reference/decision-index.yaml`.
