---
name: docs-orientation
description: "Use docs/intent plus targeted code verification to orient in a service area or workflow before editing code or making behavioral claims."
argument-hint: "Describe the service, workflow, or question to understand"
---

# Documentation Orientation Skill

This illustrative generated artifact shows what the split orientation skill can look like after bindings are resolved for the anonymized service platform.

## Porting Metadata

Ported from RepoBrain Skill Blueprint
Blueprint version: 2026.05.06
Blueprint source ref: example-blueprint-ref
Ported on: 2026-05-06

## Goal

Build a correct mental model of an API, worker, or shared-library workflow by reading the local intent docs first and then verifying the relevant behavior in code.

## Invoke When

- You need context before editing code in `services/api/src/`, `services/worker/src/`, or `packages/shared/`.
- You need to explain the purpose or behavior of a documented area under `docs/intent/`.
- You need to turn local docs into a concrete code-reading plan.

## Avoid When

- The real task is to refresh docs after a branch, pull request, or commit range.
- The user is asking for exhaustive file inventory instead of scoped orientation.

## Load First

- `AGENTS.md`
- `docs/system-overview.md`
- `docs/intent/index.md` and the most relevant doc under `docs/intent/`
- `.agent/notes/docs-skill-port.md` if present

Treat local docs as intent summaries, not runtime truth.

## Procedure

1. Establish the narrowest plausible scope from the request.
2. Read the relevant `docs/intent/` entry before broad code search.
3. Convert the docs into likely code entry points using the local seed patterns `main.ts|index.ts|router.ts|handler.ts`, `router\.|app\.use|queue\.process|register`, and `process\.env|getConfig\(|config\.`.
4. Verify the relevant behavior in `services/api/src/`, `services/worker/src/`, or `packages/shared/`.
5. Widen into adjacent components only if the answer depends on shared config, shared libraries, or cross-service flow.

## Output Contract

State:

- documented intent
- verified current behavior
- uncertainty or doc drift
- the concrete next code locations worth reading

## Validation

Before finishing, confirm that:

- repository-wide rules were loaded before local interpretation
- no literal placeholder markers remain
- the explanation does not treat docs as runtime truth
- the result points to concrete code paths such as `services/api/src/orders/` or `services/worker/src/notifications/`
