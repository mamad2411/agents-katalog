---
name: architect-review
description: Review Architect track work or explicit current changes against project context, track intent, style guides, and tests. Use when the user asks to review, verify, audit, inspect, approve, or apply review fixes for Architect-managed work.
---

# Architect Review

Perform a findings-first principal-engineer review of a track or explicit change scope. Follow `references/review-protocol.md` as the source of truth.

## Hard Boundaries

- Require Architect context for track review; warn before limited non-track review without it.
- Adopt exact or high-confidence scope without reconfirmation; ask once only for ambiguity.
- A review request does not authorize fixes. `Apply Fixes` authorizes only reported findings.
- Commit, archive, or delete only with the protocol's explicit authorization.

## Run

1. Read `references/review-protocol.md` and classify track versus non-track scope.
2. Adopt or confirm scope once, load applicable context, and derive the diff with recorded confidence.
3. Review plan, product, stack, style, correctness, security, maintainability, and tests.
4. Return findings first, ordered by severity, with verification and residual risk.
5. Apply and record only authorized fixes.
6. Offer cleanup only for an eligible track and require exact confirmation for destructive actions.
