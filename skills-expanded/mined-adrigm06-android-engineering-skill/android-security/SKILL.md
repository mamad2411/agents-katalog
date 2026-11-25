---
name: android-security
description: Android security engineering skill for threat-aware recommendations on secrets handling, secure storage, network hardening, Play Integrity, and release safeguards. Use this whenever security posture or sensitive data handling is in scope.
---

# Purpose

Provide threat-aware Android security recommendations that reduce exploitability risk while remaining operationally feasible.

## Scope and authority

This skill has global critical override authority for:

- exploitable security risk
- sensitive data exposure pathways
- secrets and trust-boundary handling

If security risk is critical, this skill can override convenience, performance, or UX preferences.

## When to use

- credentials/tokens/PII handling
- secure storage and network hardening decisions
- integrity/tamper-risk mitigation planning
- security assessment of architecture/build/release changes

## Decision engine workflow

1. Identify assets, trust boundaries, and attacker capabilities.
2. Rank threats by exploitability and business impact.
3. Choose mitigations by risk reduction vs operational cost.
4. Define rollout controls and residual risk.
5. Align with release constraints and incident readiness.

## Branching decision tree

### Branch A: risk class

- `Critical exploitability`:
  - block release-impacting exposure
  - enforce immediate mitigation path
- `High but non-blocking`:
  - prioritize near-term remediation with guardrails
- `Medium/Low`:
  - schedule hardening with explicit risk acceptance notes

### Branch B: mitigation feasibility

- if ideal control is operationally heavy:
  - recommend staged mitigation plan with interim control
- if threat model is weak/unknown:
  - choose conservative baseline controls and request missing threat inputs

## Quantitative gates

Use measurable risk gates and label each `pass | at-risk | fail`:

- unresolved critical exploitability gate (must pass for release)
- sensitive data exposure gate (must pass for release)
- control coverage gate (critical assets mapped to active controls)
- observability gate (security-relevant detection/alert paths in place)

If threat evidence is incomplete, return a measurement and threat-model completion plan first.

## Tradeoff realism

Allow constrained compromises only when explicit:

- interim controls are acceptable if expiry criteria is defined
- partial hardening is acceptable when release windows are tight and residual risk is transparent

Do not frame risk acceptance as risk elimination.

## Uncertainty protocol

Always report confidence:

- `High` (>= 0.80)
- `Medium` (0.60-0.79)
- `Low` (< 0.60)

If confidence is medium/low:

- list assumptions and missing threat intel
- provide least-risk interim control
- escalate to `android-release-engineering` when residual risk may block release
- escalate to `android-architecture` when control requires structural change

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-security`.

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

Also include:

- `Risk summary`
- `Threat surfaces`
- `Mitigation plan`
- `Storage/network/integrity controls`
- `Residual risks`
- `Implementation priorities`

## Anti-pattern detection

- secrets in source, resources, or build scripts
- plaintext sensitive data persistence
- custom crypto without strong justification
- UI-only security checks lacking backend enforcement
- security controls that are impractical to operate and therefore bypassed

## Related resources

- `references/mobile-threat-model.md`
