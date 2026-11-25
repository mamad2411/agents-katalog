---
name: repo-map
description: "Scan or query repository assets, relationships, coverage, and drift; not routine task-local file discovery."
---

# Repository Map

## Entry Gate

Own bounded repository asset scan, graph query, coverage/drift check, and derived
navigation rendering. Require a compatible graph runtime, repository root, safe scope,
and exact basis. Never substitute a hand-written map when the runtime is unavailable.

## Route Map

| Request condition | Read | Result |
| --- | --- | --- |
| Build/refresh an unambiguous graph snapshot | [graph operation gates](references/graph-operation-gates.md) and [usage](references/usage.md) | Validated bounded snapshot |
| Query identity, relation, consumer, impact, authority, coverage, conflict, or drift | [graph operation gates](references/graph-operation-gates.md) and [usage](references/usage.md) | Basis-qualified compact result |
| Root ownership or bounded source resolution is ambiguous | [ambiguity checklist](references/checklist.md) | Resolved bounded roots/source or safe stop |
| Need language/profile extraction detail | [frontend inventory](references/frontend-inventory.md), [API contract map](references/api-contract-map.md), and/or [Java build map](references/java-build-and-dependency-map.md) | Profile-specific graph evidence |
| Cross-project/repository signal applies | [project grounding](references/project-grounding.md) | Qualified boundary result |
| Render requested navigation view | [prompt templates](references/prompt-templates.md) | Derived, disposable view |

## Invariants

- Reject scope escape; isolate and exclude run-local cache from scans.
- A graph/query miss is bounded `Not found`, never proof of absence; stale snapshots remain stale.
- Index native authorities without copying or authoring repository guidance, product/design contracts, source, runtime facts, or Git state.

## Output Map

Return capability/version, basis, scope/exclusions, snapshot/query identity, coverage,
unresolved/conflict/stale state, and `Not verified` boundaries; renders name their input.

## Reference Map

- Read [graph operation gates](references/graph-operation-gates.md) for every scan/query. Read [ambiguity checklist](references/checklist.md) only when root ownership or bounded source resolution is ambiguous.
- Read [usage](references/usage.md) for route examples and owner boundaries.
- Read [frontend inventory](references/frontend-inventory.md), [API contract map](references/api-contract-map.md), [Java build map](references/java-build-and-dependency-map.md), [project grounding](references/project-grounding.md), [reuse index](references/reuse-index.md), and [prompt templates](references/prompt-templates.md) only when applicable.
- Read [Project guidance](references/project-guidance.md) only to recognize and reroute an explicit guidance create/bootstrap/update request; never use it as authoring instructions in `repo-map`.
- Maintainers only: read [eval cases](references/eval-cases.md); do not load it during ordinary runtime.
