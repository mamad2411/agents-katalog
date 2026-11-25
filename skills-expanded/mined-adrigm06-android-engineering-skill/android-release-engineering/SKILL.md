---
name: android-release-engineering
description: Android release engineering skill for signing, rollout strategy, release readiness, monitoring, and rollback planning. Use for production release planning and go/no-go decisions.
---

# Purpose

Ensure safe Android production releases through readiness validation, staged rollout control, and explicit rollback policy.

## Scope and authority

This skill is production gate authority for:

- release go/no-go decisions
- staged rollout and monitoring guardrails
- rollback criteria and incident gating

## When not to use

- when the task is root-cause analysis without release decision pressure (`android-debugging`)
- when the task is primarily architecture refactoring strategy (`android-architecture`)

## When to use

- release candidate readiness checks
- rollout and rollback strategy decisions
- cross-skill conflicts near production windows

## Decision engine workflow

1. Assess release readiness and blocker status.
2. Validate build/signing/environment integrity.
3. Determine rollout branch by risk profile.
4. Define monitoring thresholds and rollback triggers.
5. Issue go/no-go with confidence and contingency path.

## Branching decision tree

### Branch A: risk profile

- `high uncertainty or elevated incident risk`:
  - reduce rollout exposure and tighten gates
- `stable metrics and low blast radius`:
  - proceed with normal staged rollout

### Branch B: conflict with other skills

- if recommendation increases release risk beyond threshold:
  - defer or scope-limit change until post-release window

## Quantitative gates

Use measurable release gates and label each as `pass | at-risk | fail`:

- crash-free sessions gate (absolute safety gate)
- ANR rate gate (absolute safety gate)
- startup/jank regression budget (relative to baseline)
- unresolved critical security gate (must pass)

If required metrics are missing, return a measurement-first plan before irreversible rollout decisions.

## Uncertainty protocol

Always report confidence (`High`, `Medium`, `Low`).
For medium/low confidence, provide safer fallback release options.

Confidence bands:

- `High` (>= 0.80)
- `Medium` (0.60-0.79)
- `Low` (< 0.60)

If confidence is medium/low:

- list unknowns that could alter go/no-go
- define minimum additional signals required to proceed
- provide a risk-reduced release plan (scope cut, slower rollout, feature-flag gating)

## Output contract

Follow global order from `../../AGENTS.md`:

1. `Context and constraints`
2. `Decision and rationale`
3. `Alternatives considered`
4. `Tradeoffs`
5. `Risks and mitigations`
6. `Confidence and unknowns`
7. `Cross-skill impacts`
8. `Next implementation steps`

Then include release-specific artifacts:

- `Release readiness status`
- `Blocking and non-blocking risks`
- `Rollout plan`
- `Monitoring plan`
- `Rollback criteria`
- `Post-release checks`

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-release-engineering`.

## Anti-pattern detection

- big-bang rollout without staged guardrails
- weak observability for crash/performance signals
- ambiguous rollback triggers
- signing or config drift across environments

## Related resources

- `references/release-gates.md`
- `templates/release-go-no-go.md`
