---
name: build-right-engineering-principles
description: Apply Build Right engineering principles as a planning, implementation, and review standard. Use when Codex is choosing technologies, service boundaries, storage models, architecture boundaries, splitting modules or features, creating public contracts, changing provider adapters, reviewing implementation quality or over-engineering risk, planning tests, handling side effects, errors, observability, security, or deciding whether markdown guidance needs enforceable checks.
---

# Build Right Engineering Principles

Use this skill as a cross-cutting engineering standard for Build Right projects.
It is not a lifecycle phase. It is a review and design lens that other Build
Right skills may load when architecture, contracts, implementation boundaries,
or engineering-quality tradeoffs matter.

## Required Reading

- Read `references/principles.md` before making or reviewing changes that touch
  technology or storage choices, architecture or service boundaries, public
  interfaces, contracts, provider adapters, generated code, package ownership,
  side effects, errors, observability, security, testing strategy,
  over-engineering risk, or enforceable policy.
- Do not load the reference for routine product capture, backlog grooming, or
  narrow content-only updates unless those topics raise engineering-risk
  questions.

## Operating Mode

1. Identify the changed or proposed engineering surface:
   requirement basis, architecture, module responsibility, dependency direction,
   contract, adapter, state shape, side effect, failure path, test, evidence, or
   policy.
2. Apply the review checklist from `references/principles.md`.
3. Separate guidance from enforceable authority. Markdown principles are
   guidance until backed by code, checks, tests, schemas, policy, or evidence.
4. Prefer the smallest correction that preserves local patterns and reduces
   real risk. Do not introduce abstraction only because a principle names one.
5. When repeated findings expose a process gap, recommend an enforcement
   surface instead of adding more prose.
6. For a consequential public interface, run the `Design It Twice` workflow in
   the reference before implementation.
7. Record significant architecture or public-contract choices in the target
   repo's normal decision surface.

## Closeout

End with the engineering result that matters:

```text
Principles applied: <areas reviewed>
Required changes: <none | concise list>
Enforcement gap: <none | check/test/schema/policy/docs evidence needed>
Residual risk: <none | concise risk>
```

## Automatic Action Boundary

Never automatically commit, push, merge, publish, deploy, or abort or resolve
an existing Git operation. Perform those actions only when the user explicitly
authorizes the exact action and target.

## User-Visible Status Badge

End every final response with exactly one status badge block:

```text
✅ [DONE] Status: DONE
Decision: <decision/result>
Next action: <next action or none>
Needs user input: <none | concise ask>
Blocked by: <none | blocker>
```

Use this status map:

- `✅ [DONE] Status: DONE` when there are no required changes and
  no enforcement gap.
- `🟢 [GREEN] Status: ALL GREEN` when the reviewed direction is safe to
  continue but implementation is not complete.
- `🟡 [YELLOW] Status: NEEDS INPUT` when a user or owner architecture,
  contract, security, or policy decision is needed.
- `🟠 [ORANGE] Status: NEEDS WORK` when AI-owned corrections, tests,
  docs, or enforcement work remain.
- `🔵 [BLUE] Status: WAITING EXTERNAL` for external proof, credentials,
  production access, publishing, indexing, or third-party state.
- `🔴 [RED] Status: BLOCKED` for unresolved conflicts, failed
  validation, source mismatch, invalid state, or enforcement blockers.
