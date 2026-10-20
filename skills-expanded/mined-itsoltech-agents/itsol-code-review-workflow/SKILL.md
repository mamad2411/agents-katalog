---
name: itsol-code-review-workflow
description: "Run ITSOL code or PR review with scoped coverage, ranked findings, risk, and verdict."
---

# ITSOL Code Review Workflow

Review as risk control: acceptance/correctness, security/data safety, compatibility/operations, verification, maintainability; style is non-blocking unless it violates policy or hides a defect.

## Extension-managed policy

- `off`: no ceremony unless explicitly requested;
- `poc`: one lightweight inline pass, no delegation or automatic rereview;
- `balanced`: main agent decides whether one proportionate inline/specialist pass adds value;
- `strict`: risk-based independent coverage and rereview after real fixes until approved or capped.

`trigger=manual` runs only on request; `adaptive` lets the main agent choose whether and how deeply; `final` runs once before completion. `delegation=never` forces inline review. Automatic rereview requires a prior material `changes-requested` verdict, changed diff fingerprint, and an available round; never exceed `max_rounds` or `execution.max_review_rounds`.

## Review

1. Read the request/acceptance, changed files, verification evidence, relevant tests, migrations, config, QA notes, and repo policy. Do not demand RED/GREEN unless test-first development was explicitly requested; assess test value from behavior protected, not test count or implementation coverage.
2. For `adaptive`, skip formal review for small, conventional, low-risk, well-verified changes and record why; use it for material scale, novelty, uncertainty, blast radius, trust/data boundaries, reversibility, or weak evidence.
3. Build only the affected coverage map: behavior, security, data/storage, infrastructure, tests, performance, observability, maintainability, release/QA.
4. Review inline or delegate by independent risk surface. Use the narrowest relevant skill and `itsol-subagent-workflow`; do not fan out because a filename matches a family.
5. Require one evidence-based result per reviewer: severity, file references, affected behavior, missing verification, assumptions, and residual risk. Consolidate duplicates and false positives.
6. Block only for a concrete defect with plausible failure path and material impact introduced by the change. Do not block on preferences, optional refactors, speculative edges, unrelated debt, or irrelevant tests.
7. Label findings `Blocker`, `Should`, `Question`, `Suggestion`, `Nit`, or `Note`; only concrete blocker/high-severity defects require changes or rereview.
8. Stop for a material scope, architecture, requirement, migration, rollout, or evidence gap that prevents a reliable verdict.

Load `itsol-execution-policy` when resource, stop, delegation, or completion state matters. It owns budgets and evidence validation; never use `maxTurns` or termination as completion.

## Focused references

- [01-overview.md](./references/01-overview.md) — review perspective.
- [02-code-review.md](./references/02-code-review.md) — review method.
- [03-handoffy-miedzy-rolami.md](./references/03-handoffy-miedzy-rolami.md) — handoffs and checklist.
- [04-multi-agent-review-gate.md](./references/04-multi-agent-review-gate.md) — mandatory mapping and subagent gate.
- [05-review-profiles-and-rereview.md](./references/05-review-profiles-and-rereview.md) — profiles, triggers, fingerprints, and rounds.
