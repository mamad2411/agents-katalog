---
name: stack-select
description: Select the technology stack (language, framework, ORM, UI kit, tooling) for the chosen architecture variant via a constrained trade study.
---

# /stack-select

Owner: **lead-architect**; frontend/backend/data leads consulted.

## Sequence
1. Precondition: architecture variant chosen (ARB passed or in progress). The variant
   constrains the stack (edge runtime ≠ arbitrary Node deps; Lambda favors fast-cold-start).
2. Candidates from `constraints/stack-registry.yaml` only — additions require a registry PR with
   sources. Compare 2-3 options per layer: language/runtime, backend framework, frontend
   framework, ORM/data access, UI approach, package manager, test runner, lint/format.
3. Criteria: fit to variant (cold start, runtime support on the target), team skills (from the
   brief — a stack the team can't maintain fails regardless of elegance), ecosystem maturity,
   hiring pool. Quantify where possible; taste is not a criterion.
4. Pin versions (major.minor) for everything chosen; record as `architecture/ADR-002-stack.md`.
5. The user decides per operation_mode.

## Output
ADR-002 with the stack table (layer, choice, version, runner-up, why); registry gaps flagged.
