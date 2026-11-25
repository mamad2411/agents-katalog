---
name: enterprise-harness
description: Use when enterprise work has been built and reviewed and needs a final mechanical ship or release gate before merge, PR readiness, install, deploy, or signoff. Checks proof trace, current diff, architecture, post-merge test kit, rollback, observability, security/privacy, and performance regression readiness.
---

# Enterprise Harness

Final quality gate for enterprise work.

Treat the harness as a fail-closed evidence gate. Schema, query, and data-sensitive changes need live/integration DB proof; UI/PDF/file changes need headless browser proof; every changed runtime file needs code execution proof, E2E trace proof, or a documented non-runtime reason. Full proof is the only pass: `PARTIALLY PROVED`, `UNPROVED`, mock-only proof, stale proof, wrong-head proof, missing intent continuity, missing touched-file SRP proof, missing DB/query ownership proof, or missing important edge-case proof fails harness. For async/order/invoice/inventory/pricing/label-printing workflows, missing exact field-spelling, preserved confirmation, commit-boundary, helper return-variant, retry, or rehydration proof is a blocking edge-case gap.

Harness also acts as the senior release-readiness gate. Before ship-ready,
PR-ready, merge-ready, install-ready, or release-level signoff, it must classify
release risk and require the matching operational proof: post-merge validation,
rollback readiness, observability, security/privacy, and performance regression
coverage where relevant. These release gates must be expressed as structured
verification records named `enterprise_release_risk`,
`enterprise_post_merge_test_kit`, `enterprise_rollback_readiness`,
`enterprise_observability_proof`, `enterprise_security_privacy_proof`, and
`enterprise_performance_regression`; `validate_release_readiness.py` is the
mechanical authority for that proof.

## When To Use

- before merge
- before installation of generated skills
- before calling a change ship-ready

## Required Behavior

Run the checks in [final-gate-checks.md](references/final-gate-checks.md) as a fresh pass over the resulting artifacts, not as a recap of what build or review already said.

Before harness starts, run the agent-bound harness gate in [agent-stage-gates.md](../enterprise/references/agent-stage-gates.md).

For merge or PR readiness, also run the stable enterprise wrapper; do not use raw repo-local gate scripts as the command surface:

```bash
enterprise-required-gates --repo-root "$PWD" --stage pr-readiness --agent-id <agent-id> --json
```

This gate fails if `enterprise-review`, `enterprise-forge`, and `enterprise-verify` were not recorded in order against the current code state or if the receipt-backed proof bundle is incomplete.

Harness also fails if the recorded `build_packet` is missing, incomplete, or no
longer covers the final changed paths. Mechanical build proof is part of ship
readiness: allowed-path coverage, RED/GREEN receipts, forbidden-change scan, and
refusal-condition status must all be present in review or verification evidence.
The packet must also cover intent-continuity rows, touched-file SRP/refactor
classifications, and DB/query ownership packets for reads, writes, reports,
migrations, verifiers, and live-proof queries.
The same packet must pass `validate_architecture_contract.py`: module boundary,
folder placement, public seam, owner layer, dependency direction, forbidden
imports, and architecture tests must be exact and evidenced before ship-ready,
PR-ready, merge-ready, or install-ready claims.

## Senior Release Gates

Harness must fail closed unless these gates are satisfied or explicitly marked
`not-applicable` with evidence:

- `release-risk-classification`: classify the lane as `low`, `medium`, `high`,
  or `critical` from the changed surfaces, affected data, blast radius, tenant,
  money/order/invoice/inventory/security exposure, migration/config/deploy
  impact, and rollback difficulty. Risk decides required proof depth.
- `post-merge-test-kit-required`: for deployable PRs, require a drafted
  `post-merge-test-kit` artifact before merge/pr-readiness, or a recorded reason
  that the change is non-deployable. High/critical deployable PRs must include
  owner, environment, deployed-SHA proof plan, and agent-run or human-run mode.
- `rollback-readiness-gate`: require rollback owner, rollback trigger,
  rollback command/procedure, feature-flag or disable path when applicable,
  migration/data rollback posture, and customer/operator communication owner for
  high/critical releases.
- `observability-proof-gate`: require exact logs, metrics, dashboards, health
  checks, queue/job/readback checks, alert signals, and watch window that will
  prove the release is healthy after deploy. "Monitor logs" is not enough.
- `security-privacy-proof-gate`: when auth, tenant scope, permissions, PII,
  secrets, payment, webhook, file upload, or external integration boundaries are
  touched, require explicit proof and redacted evidence. Secret-bearing evidence
  fails the harness.
- `performance-regression-gate`: when hot paths, queries, workers, syncs,
  rendering, PDF/file flows, or high-volume loops are touched, require a
  regression budget and proof for latency, query plan/index safety, queue
  backlog, timeout/retry behavior, or a documented not-applicable reason.
- `intent-continuity-gate`: require proof that the final diff still satisfies the
  original user words, business outcome, operator acceptance, and non-goals from
  the intake/design. Generic suite PASS is not enough.
- `touched-file-srp-gate`: require proof that each changed file's SRP assessment
  was honored, including contracted `fix-now` refactors for mixed-responsibility
  touched files.
- `db-query-ownership-gate`: require owner-seam, current DB/schema, scoping,
  affected-row/readback, bounded proof, cleanup, and redaction evidence for every
  DB/query path, including read-only SELECT/report/verifier/live-proof queries.
- `last-150-trap-closure-gate`: for PR-producing or branch-window retrospective
  work, require structured evidence that every applicable recent trap-bank row is
  closed by a current-head ratchet, proof command, gate, or explicit source-backed
  non-goal. Stale UI/read-model rehydration, config/env/outage semantics,
  proof-lane selector false greens, stale proof-subject/preflight failures, weak
  assertions, DB/query ownership gaps, integration side-effect/idempotency faults,
  redaction/diagnostic leaks, and SRP/domain-boundary drift cannot be waived by a
  broad test-pass summary.

Before a PASS verdict, run:

```bash
python3 ~/.codex/skills/enterprise-harness/scripts/validate_release_readiness.py --evidence <verification-artifact> --json
```

Missing records, vague `not-applicable` reasons, secret-bearing evidence, and any partial-proof verdict are
blocking failures.

## Output

Produce a compact `PASS` or `FAIL` verdict with exact failing checks and the blocking reason. Use `FAIL` for every missing gating record, partial proof, stale proof, unsafe DB target, missing intent-continuity proof, missing touched-file SRP proof, missing DB/query ownership proof, or unproven release-readiness cell; do not downgrade gate gaps to `WARN`.

For enterprise skill updates based on PR retrospectives, include a baseline-vs-updated behavioral proof summary from old-skill and updated-skill runs. Static file coverage, keyword checks, and deterministic assertion coverage are supporting evidence only; they cannot justify a `PASS` or `done` claim for "the skill would have caught the issue" unless model-run behavioral testing is blocked, the blocker is recorded, and the verdict is kept no stronger than `BLOCKED`/`PARTIAL`. List each eval prompt, old verdict, new verdict, assertion delta, and remaining unproven trap classes.
