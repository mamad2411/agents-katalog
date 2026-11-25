---
name: helpdesk-quality-gates
description: Apply final Claude/Codex consensus quality gates for Helpdesk PRs, goals, skills, and workflows before claiming ready, green, done, merge-ready, or workflow-complete.
---

# Helpdesk Quality Gates

Use this skill as the final quality gate layer for Helpdesk work. It does not
replace repo route cards, enterprise gates, `patch-or-fix`, `prove-it`, PR
checks, review-thread closeout, or local runtime proof. It forces those signals
into durable, current-head artifacts before any completion claim.

## Operating Rule

Fail closed. If a gate cannot be proven from current source, current PR head,
runtime evidence, or an explicit artifact, mark the work `BLOCKED` or
`UNPROVEN`. Do not downgrade a hard gate into a reminder, TODO, checklist item,
or narrative caveat.

Run these gates before:

- Saying a Helpdesk PR, goal, skill, workflow, or agent lane is ready, green,
  done, merge-ready, ship-ready, or complete.
- Creating or approving a PR-ready handoff.
- Closing a bugfix, workflow hardening, skill authoring, or enterprise lane.

## Progressive Disclosure

Keep this file as the routing layer.

- Use `scripts/validate_quality_artifact.py` when a quality-gate artifact,
  ledger, or template output exists and must be validated deterministically.
- Use `templates/*` only for the specific artifact shape requested by the task:
  ownership ledgers, goal contracts, PR proof ledgers, proof matrices,
  falsification records, executable contracts, failure paths, or hard-gate
  checklists.
- Do not read every template by default. Pick the one matching the requested
  deliverable or the missing gate.
- If the validator or a needed template is absent, report the missing resource
  as a blocker for machine validation, then apply the gate manually from this
  file without inventing a substitute format.

## Required Inputs

Resolve the smallest current evidence bundle that can prove the claim:

- Repo path, branch, base branch, current SHA, PR number if any, and target
  environment.
- Route card, enterprise preflight/readiness artifact, or declared `NO_EDIT`
  status when applicable.
- Current diff or PR diff, plus changed files and owned boundaries.
- Current tests, local canary, runtime, DB/schema, browser, or integration
  evidence required by the risk tier.
- Review-thread, CI, mergeability, and deployment state when the claim touches
  PR or ship readiness.

## The Eight Consensus Gates

### 1. Ownership Ledger Before First Diff

Before code or workflow edits begin, produce or locate an ownership ledger.
It must name:

- The owned behavior or invariant.
- The file, domain, route, workflow, skill, or agent lane that owns it.
- Allowed edit paths and forbidden paths.
- Upstream writers, downstream consumers, sibling paths, and known recurrence
  risks.
- The proof surface that will show the owner actually enforces the invariant.

No first diff is acceptable without this ledger unless the route is explicitly
`NO_EDIT`. For already-started work, create the ledger before the next diff and
classify any prior edits against it.

### 2. Goal Contract With Terminal State, Acceptance, And Rollback Or Block Trigger

Every goal or lane must have a written contract with:

- `terminal_state`: the exact state that ends the lane.
- `acceptance_condition`: observable proof that the terminal state is reached.
- `rollback_trigger` or `block_trigger`: the concrete condition that forces
  revert, stop, escalation, or a new scoped lane.

Do not accept vague terminal states such as "fix issue", "make green", or
"address comments". The terminal state must say what branch, PR, environment,
artifact, or runtime behavior is proven.

### 3. Generated Current-Head PR Proof Ledger

For PR-related claims, generate or refresh a proof ledger against the current PR
head SHA. It must include:

- PR number, base branch, head branch, head SHA, author identity, and timestamp.
- Required checks and their current result.
- Review-thread count and unresolved thread list, or direct proof that none
  remain.
- Mergeability and merge-state evidence.
- Blast-radius, regression, edge-case, and conversations-addressed evidence.
- Runtime or local proof tied to the same head SHA, or an explicit stale-proof
  blocker.

Green checks alone do not satisfy this gate. A new commit invalidates prior PR
proof until the ledger is regenerated.

### 4. Risk-Tiered Proof Matrix

Choose the proof tier from actual blast radius, not convenience.

- `low`: docs, copy, narrow tests, or mechanical skill text. Require source
  review plus focused validation or explicit no-runtime-impact rationale.
- `medium`: multi-file code, UI behavior, route logic, async jobs, worker flows,
  or shared helpers. Require focused tests plus one realistic boundary proof.
- `high`: data correctness, inventory, pricing, auth, tenant isolation,
  migrations, concurrency, payments, invoicing, destructive actions, or
  cross-service failure modes. Require source proof, tests, live-schema or
  integration proof where safe, rollback/block plan, and adversarial review.

If a lower tier is chosen, state why excluded higher-risk categories are not in
scope. Missing proof keeps the status no higher than `PARTIALLY_PROVED`.

### 5. Falsification Proof For Bug Fixes

Bug fixes need an attempt to disprove the fix. Record:

- The original symptom and root-cause chain.
- The invariant that should prevent recurrence.
- Active entry points that could still create the bad state.
- Sibling states, fallbacks, swallowed errors, stale caches, race windows, and
  alternate writers reviewed.
- The test, canary, browser flow, DB query, log, or code path that would fail if
  the fix were only a symptom patch.

If falsification cannot be attempted, the bugfix remains `UNPROVEN`. If the
attempt finds another active path to the same class of bad state, classify the
result as `PATCH` or `PARTIAL FIX`.

### 6. Executable Skill And Agent Contracts

Skills, workflows, and agent handoffs must be executable by another Codex agent
without transcript-only context. The contract must include:

- Trigger or invocation conditions.
- Required inputs and forbidden assumptions.
- Exact artifacts to read or produce.
- Commands, validators, wrappers, or MCP tools to run when applicable.
- Stop conditions, failure states, and what must not be automated.
- Expected output shape.

Prefer validator-backed artifacts over prose. A contract that cannot be executed
or checked is not complete.

### 7. Explicit Failure Path

Every quality-gated lane must name the failure path:

- What status to emit on missing evidence.
- What artifact or command proves the blocker.
- Whether to stop, revert, split scope, create a follow-up issue, ask Ben, or
  hand off to another lane.
- What must not be claimed while blocked.

Do not bury failure handling in caveats. The final answer or artifact must make
the blocker operational.

### 8. Hard Gates Over Reminders

Convert reminders into enforcement:

- Use wrappers, validators, required artifacts, CI checks, route-card gates, or
  PR-body requirements where possible.
- Treat missing generated ledgers, stale SHAs, unresolved threads, route-card
  violations, forbidden paths, and skipped high-risk proof as stop conditions.
- Do not rely on "remember to", "should", "consider", or "follow up later" for
  correctness boundaries.

If enforcement is not yet automated, name the manual hard gate and the exact
evidence required to pass it.

## Output

Return the lowest honest verdict:

```markdown
**Quality gate verdict:** PASS | PARTIAL | BLOCKED | FAIL
**Current target:** <repo/branch/pr/sha/env or missing>
**Risk tier:** low | medium | high
**Gates passed:** <gate numbers and proof>
**Gates blocked or failed:** <gate numbers and exact missing/failed evidence>
**Validator:** <command/result or not run and why>
**Next required action:** <one concrete action>
```

Only emit `PASS` when all eight gates are satisfied for the current target and
the proof is tied to the current source or PR head.
