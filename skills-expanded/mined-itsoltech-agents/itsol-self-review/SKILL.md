---
name: itsol-self-review
description: "Self-review plans or code for correctness, tests, edge cases, security, UX, and risk."
---

# ITSOL Self Review

Resolve and validate `itsol-workflow-mode` before review; preserve all seven state fields. Run a concise final review before claiming completion. Use isolated Rubber Duck review for Business/Technical Plans only when policy or material scale, uncertainty, novelty, or risk justifies it.

## Review contract

1. Re-read the artifact and relevant repo policy; load `itsol-repo-memory` when `.itsol.md` exists.
2. For plans, challenge only omissions that can change scope, acceptance, correctness, safety, feasibility, rollout, or verification. Do not demand exhaustive detail for conventional work.
3. Validate authorization: governed requires user-seen `Approved`; autonomous-planned accepts material-blocker-free delegated `Ready for execution`; direct accepts `not-required` and reviews implementation evidence instead. Reject false approval claims.
4. For code, check requirements, changed behavior, edge cases, permissions, validation, data consistency, errors, observability, rollout, and scope expansion. Confirm proportionate verification of material behavior; missing RED/GREEN or a TDD exception is not a finding. Challenge trivial, duplicated, mock-call, or implementation-detail tests that add maintenance cost without protecting a contract.
5. For subagent work, validate status, scope/files, evidence, assumptions, unverified items, coverage gaps, risks, blockers, and next review target. Focused domain review is conditional, not default fan-out.
6. Report blockers, meaningful gaps, verification commands, risks, and `partial`/`blocked`/`failed` items. A blocker needs concrete impact and a plausible failure path introduced by the work.

## Plan review

Do not edit the plan. Return one report containing inspected context, material blockers, invalid authorization, hidden assumptions, weak acceptance/verification, missing technical or subagent packet details, required user questions, sections to update, and the mode-specific verdict:

- governed: `ready for approval` or `not ready for approval`;
- autonomous-planned: `ready for execution` or `not ready for execution`;
- direct: no plan-review verdict.

Use `not ready` only for a concrete material defect. Wording, style, optional detail, speculation, preferences, and unrelated legacy debt are non-blocking and must not trigger another round.

## Independent review

Consider focused subagents for material security/data/infra blast radius, broad cross-cutting behavior, novelty, reversibility, or a diff too large for one reliable context. Keep small conventional changes inline. Split only independent surfaces; the main agent consolidates duplicates, false positives, conflicts, and the final verdict. Preserve genuine incomplete statuses and gaps; do not promote harmless uncertainty into blockers.

Load `itsol-execution-policy` when resource, stop, delegation, or completion state matters. It owns budgets and evidence validation; never use `maxTurns` or termination as completion.

## Focused references

- [01-overview.md](./references/01-overview.md) — self-review, PR, and risk.
- [02-checklista-dla-nowej-funkcjonalnosci.md](./references/02-checklista-dla-nowej-funkcjonalnosci.md) — feature/bugfix checklist and edge cases.
- [03-nawyki-dobrego-dewelopera.md](./references/03-nawyki-dobrego-dewelopera.md) — completion and review habits.
