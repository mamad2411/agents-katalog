---
name: build-mobile-apps
description: Use when implementing or reviewing cross-platform mobile frontend code and you need a repeatable workflow for architecture, accessibility, resilience, performance, and release readiness.
---

# Build Mobile Apps

## Specialization

Implement and review cross-platform mobile frontend work using deterministic, evidence-first checks across architecture, UX quality, resilience, and release hardening.

## Trigger Conditions

Use this skill when one or more are true:
- The request targets mobile frontend implementation across iOS and Android.
- The work spans navigation, state, data flow, accessibility, or performance.
- The request needs release-facing validation evidence for a mobile change.

## Required Inputs

- Target platform scope and feature boundary.
- Existing UX or acceptance requirements.
- Data contracts, API endpoints, and offline expectations.
- Release constraints (signing, rollout, rollback).

## Required Outputs

- Mobile implementation changes aligned to platform parity and accessibility baseline.
- Validation evidence for behavior, resilience, and performance-sensitive paths.
- Explicit release-readiness recommendation with open risks and owners.

## Workflow

1. Confirm scope, user flow, and platform parity requirements.
2. Implement the smallest safe change set for the requested behavior.
3. Validate accessibility and error/empty/loading states.
4. Validate degraded-network and recovery behavior.
5. Validate performance-sensitive interactions and startup impact.
6. Publish outcomes, residual risks, and follow-up actions.

## Quality Gates

- Accessibility: focus order, semantic labels, and actionable error feedback are present.
- Resilience: network interruptions and retries are handled without data loss.
- Performance: no obvious regressions in startup or primary interaction latency.
- Security: no secrets in code or logs; sensitive storage is protected.

## Done Criteria

- Requested mobile behavior is implemented and verified.
- Required output evidence is documented.
- Remaining risk items are explicit, prioritized, and owner-assigned.
