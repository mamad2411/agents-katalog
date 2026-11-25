---
name: plan-360-audit
description: Use when a plan, design, migration, or deployment checklist is drafted and needs review before passing a planning gate or proceeding to implementation. Triggers on phrases like "review this plan", "is this ready", "gate check", "audit the plan", "stakeholder review", or whenever a document in docs/plans/, .claude/designs/, or docs/handovers/ is about to be acted on. Also use proactively before any implementation begins. Every plan must pass stakeholder audit, enterprise architecture review, and root-cause structural review before code is written; plans that do not prove root cause, ownership, SRP/cohesion, domain boundaries, correct seams, fix-now refactors, and recurrence guards must fail.
---

# Plan 360 Audit

## Overview

Every plan must survive scrutiny from every direction before a single line of code is written. This skill stress-tests plans, designs, migrations, and deployment checklists from three dimensions:

1. **Stakeholder 360** — Would this plan work for everyone it touches? Not just the developer, but the accountant, the warehouse operator, the customer, the supplier, the support agent.
2. **Enterprise Architecture Gate** — Is this built to enterprise standards, or is it "just making it work"? Enterprise-grade means observable, scalable, auditable, recoverable, and secure by default — not gold-plated after the fact.
3. **Root-Cause Structural Gate** — Does this plan remove the cause of the defect or need, at the owning boundary, with SRP/cohesion, domain ownership, correct seams, fix-now refactors, and recurrence guards proven before implementation?

The philosophy: **we don't ship fixes then harden later. We build enterprise-level systems from the start.** When someone reviews our code, they should see deliberate architecture, not vibe-coded solutions.

## Non-Negotiable Approval Standard

A plan is not ready because it is plausible, well-written, or stakeholder-aware. It is ready only when it proves the system-level change that will make the desired outcome true and prevent the same class of failure from returning.

`PASS` is forbidden when any of these are missing, stale, or contradicted:

- **Root cause**: the plan names the exact broken invariant, missing capability, or ownership failure it is addressing, with current source/runtime evidence.
- **Owning boundary**: the plan names the domain/service/repository/policy/schema/contract that owns the rule and shows every active entry point delegates there.
- **SRP/cohesion**: touched units keep one primary reason to change; overloaded files or mixed route/UI/worker/service responsibilities on the defect path are classified as `FIX-NOW`.
- **Domain boundary**: business invariants live in domain-owned code or typed contracts, not route glue, UI handlers, scripts, fixtures, one-off SQL, or tests.
- **Correct seam**: the plan identifies the smallest real seam where the invariant can be tested or enforced without driving through unrelated layers.
- **Refactor requirement**: structural work is classified as `FIX-NOW`, `FOLLOW-UP`, or `NOT NEEDED`; `FIX-NOW` cannot be deferred into a condition or later phase.
- **Recurrence guard**: the plan includes a regression test, invariant check, contract, schema constraint, ownership gate, canary, or deleted duplicate path that would fail if the same class of bug returns.
- **Falsification**: the plan says how to prove the old failure cannot be produced through every active entry point, and how adjacent/sibling flows stay correct.
- **Fresh evidence**: code, schema, route, runtime, migration, and proof claims are verified against the current checkout/runtime, not plan prose, memory, old PRs, or mocks when stronger evidence is available.
- **Assumption control**: assumptions that affect root cause, ownership, SRP, domain boundaries, seams, recurrence, rollout, or stakeholder impact are named and proven, or the plan fails closed.

If a plan mostly handles the bad state after it exists, leaves the rule in a consumer layer, duplicates logic across callers, or relies on future implementers remembering to copy the same guard, verdict must be `FAIL`.

## When to Use

- Before passing any planning gate (brainstorm → plan, plan → implementation)
- Before the final gate into implementation
- When reviewing migration plans, deployment checklists, or design docs
- When you feel a plan is "done" — that's exactly when it needs this audit

## Process

### Step 1: Identify the Document

Read the plan/design/migration being audited. Understand its scope, goals, and proposed approach.

### Step 2: Discover Affected Stakeholders

Don't use a fixed list. Derive stakeholders from the plan itself by asking:

- **Who touches this system?** (developers, ops, support)
- **Who sees the output?** (customers, suppliers, internal users)
- **Who pays for it?** (finance, accounting, management)
- **Who supports it?** (support agents, on-call engineers)
- **Who audits it?** (compliance, security, external auditors)
- **Who depends on it downstream?** (integrations, reporting, other teams)
- **Who is affected indirectly?** (end customers whose orders flow through this, partners whose data changes)

Common stakeholder categories (use as seeds, not a checklist):

| Category | Example Roles | What They Care About |
|----------|--------------|---------------------|
| Financial | Accountant, CFO, bookkeeper | Cost, tax implications, margins, reconciliation, audit trail, reporting accuracy |
| Operational | Warehouse, logistics, support | Workflow disruption, training, edge cases, manual overrides, daily routine changes |
| Customer-facing | End customer, guest, B2B buyer | UX clarity, communication, self-service, error recovery, order accuracy and timing |
| Supplier/Partner | Supplier, vendor, integration partner | Data accuracy, API contracts, notification timing, portal experience |
| Technical | Developer, DevOps, on-call | Maintenance burden, observability, deployment risk, rollback, debugging at 3am |
| Compliance | Legal, security, privacy | Data handling, access control, retention, regulation, audit completeness |
| Strategic | Owner, product lead | Alignment with direction, ROI, opportunity cost, incremental value delivery |

**The customer trap:** Technical plans naturally focus on the builder's perspective. The most commonly missed stakeholder is the end customer — the person whose order, payment, or experience flows through this system. Even backend-only changes can affect order timing, notification accuracy, or error messages that reach customers. Always ask: "Does this change affect anything a customer eventually sees, receives, or experiences?" If yes, include them.

**The reporting trap:** Changes to data schemas, status values, timestamps, or calculation logic can silently break reports, dashboards, and exports that finance/management rely on for decisions. If the plan touches any data that feeds reporting, the financial stakeholder must be included — even if the plan is "purely technical."

### Step 3: Dispatch Stakeholder Audits (Parallel)

For each identified stakeholder perspective, dispatch a subagent that:

1. Reads the plan from that stakeholder's viewpoint
2. Identifies concerns, risks, and gaps specific to their role
3. Rates severity: BLOCKER / HIGH / MEDIUM / LOW
4. Suggests mitigations for each concern

Each subagent prompt should include:
```
You are reviewing this plan as a [ROLE]. Your job is to find problems
that someone in this role would care about. Be specific — don't flag
generic risks, flag concrete issues with this specific plan.

Think about:
- What could go wrong for you specifically?
- What information is missing that you'd need?
- What assumptions does this plan make about your domain?
- What edge cases would hit you hardest?
- Would this plan survive your audit/review process?
```

**The grounding rule — no unanchored concerns:**

Every concern you raise must cite a specific section, quote, file, or detail from the plan. If you can't point to where in the plan the problem originates, the concern is too generic to be useful. "No rollback strategy" is weak. "Phase 1 migration (migrations 351-353) uses `DROP TABLE ... CASCADE` with no rollback step or backup mentioned" is strong — it points to the exact phase and operation.

**The code verification rule — read before you flag:**

If a concern involves code (files the plan mentions, services it proposes to change, migrations, endpoints, existing abstractions), you must read the actual source files before raising the concern. Plans regularly contain stale information — wrong file counts, missed existing abstractions, outdated line references, migration number collisions. The only way to catch these is to verify against the codebase. Specifically:

- If the plan says "update 47 files" — grep and count the real number
- If the plan proposes creating a new service — check if one already exists that does the same thing
- If the plan references migration numbers — check what migrations already exist
- If the plan claims a function works a certain way — read the function
- If the plan says a table has N rows or columns — verify the schema

An audit that doesn't verify code claims is just reviewing the plan's marketing copy. The highest-value findings come from the gap between what the plan says and what the code actually is.

**Mandatory verification commands — paste the output, do not summarise:**

PR #1796 (2026-05-14) was declared scope-lock by four plan audits and two code reviews, then ten findings landed on the PR within minutes — including one P1 (`collectHealthMetricsUncached` mutating the DB while a GET route still called it). Every miss was a one-line `grep` away. To prevent recurrence, the following five sweeps MUST run, AND the audit document MUST include the output verbatim. A concern raised without these greps is too shallow. A PASS verdict without these greps is invalid.

1. **Caller trace** — every exported function or module API the diff touches:
   ```bash
   for fn in <list-the-exports-the-diff-modified>; do
     echo "=== $fn ==="
     grep -rn "\\b$fn\\b" apps/api/src --include='*.js' | grep -v '__tests__'
   done
   ```
   For every caller listed, verify the new semantics of the function are still safe for that caller. **A function that gains a side effect (DB mutation, network call, filesystem write, queue insert) is a contract change for every caller, not just the one named in the plan.** GET routes calling a now-mutating function = P1.

2. **Endpoint / route contract** — every URL or path mentioned in the plan, runbook, or implementation:
   ```bash
   grep -rn "<path-pattern>" apps/api/src/routes --include='*.js'
   ```
   Open the matched route file and verify (a) what each `:param` actually binds to (UUID? rex id? slug?), (b) which middleware/auth gates apply, (c) what the handler returns. Plans that say "POST /api/x/:id with rex_product_id" where `:id` is actually a UUID column = operator/dev calls it wrong on day one.

3. **Test-helper survey** — before writing new test infra:
   ```bash
   ls apps/api/src/__tests__/helpers/
   grep -rln "primeTestDatabaseUrl\\|beginRollbackScope\\|liveDbContractHarness" apps/api/src/__tests__/
   ```
   If the project has a canonical helper for the pattern you are adding, use it. Parallel infra that bypasses the project's standard test harness is a review finding.

4. **Render-vs-doc skew** — when the diff includes a renderer + a runbook/doc:
   ```bash
   grep -E "row\\.|metrics\\." apps/api/src/<renderer-file> | sort -u
   ```
   Walk every step of the runbook against the rendered fields. If the runbook says "use the on_hand value from the email" but the renderer never emits on_hand, that's a finding.

5. **Post-rename stale-reference sweep** — whenever a file or symbol is renamed in the diff:
   ```bash
   git diff --diff-filter=R --name-status <base>..HEAD
   # then for each renamed file:
   grep -rn "<old-name>" docs/ apps/ --include='*.md' --include='*.js' --include='*.sql'
   ```
   The post-rename file's own header comments, JSDoc, and SQL comment blocks frequently still cite the old name. Catch them here.

These five commands are not optional. They are the difference between a narrative review and a verification review. The 2026-04-18 ord-column promotion and the 2026-05-14 PR #1796 P1 both happened because reviewers used the plan as a source of truth instead of the codebase.

### Step 4: Root-Cause Structural Gate

Run a separate structural assessment before the enterprise gate. This gate borrows the strict fix lenses from `$diagnose` and `$patch-or-fix`: plans must remove why the problem happens, not only change what happens after it appears.

#### Required Root-Cause Questions

Answer each question with plan evidence and source/runtime evidence:

- What symptom, workflow failure, or desired outcome is the plan addressing?
- What immediate behavior creates the symptom or blocks the outcome?
- What deeper missing invariant, owner, contract, seam, or lifecycle rule allows that behavior?
- Which module/service/table/domain owns the rule today, and which module should own it after the plan?
- Which active entry points can produce the same bad state: routes, UI actions, jobs, webhooks, scripts, scheduled tasks, imports, external callbacks, or direct writes?
- Which writers are allowed to mutate the owned state, and which consumers are allowed to read or project it?
- What public boundary contract enforces the rule: exported method, repository method, DTO, API schema, queue payload, event, schema constraint, policy module, or ownership registry?
- Which non-owner layers must not copy or carry the rule?
- What `FIX-NOW` SRP, ownership, domain, or seam refactor is required before implementation can safely proceed?
- What ratchet proves recurrence prevention?

#### Evidence and Assumption Ledgers

Every structural approval claim must be backed by a ledger row. If a claim is not in the ledger, it cannot support `PASS` or `CONDITIONAL PASS`.

```markdown
| ID | Claim | Evidence | Source/command | Result |
|---|---|---|---|---|
| E1 | [claim] | [plan section, file:line, command output, schema/runtime proof] | [read/run/query/action] | PROVEN/CONTRADICTED/UNPROVEN |
```

```markdown
| ID | Assumption | Evidence check | Status |
|---|---|---|---|
| A1 | [assumption] | [evidence ID or missing proof] | PROVEN/CONTRADICTED/UNPROVEN |
```

Evidence `Result` and assumption `Status` must use only `PROVEN`, `CONTRADICTED`, or `UNPROVEN`. `PASS` and `CONDITIONAL PASS` are forbidden when a required claim or assumption is `CONTRADICTED` or `UNPROVEN`.

#### Boundary Ledger

Every audit must include this table. If any column is unknown for a plan that touches behavior, data, schema, routes, jobs, UI workflows, integrations, or owned state, the maximum verdict is `FAIL`.

```markdown
| Invariant / rule | Correct owner | Active entry points | Allowed writers | Allowed consumers | Boundary contract | Forbidden non-owner layers | Result |
|---|---|---|---|---|---|---|---|
```

Result must be `PASS`, `FAIL`, or `UNPROVEN`. `PASS` requires source-proven ownership and a plan that routes all active entry points through one owner. A shortened ownership table is not acceptable.

#### Structural Checks

Every audit must include this table:

```markdown
| Check | Result | Evidence | Required action |
|---|---|---|---|
| Root cause | PASS/FAIL/UNPROVEN | [plan section + source/runtime proof] | ... |
| Ownership | PASS/FAIL/UNPROVEN | [owner + callers/writers/consumers] | ... |
| SRP/cohesion | PASS/FAIL/UNPROVEN | [touched units + responsibilities] | ... |
| Domain boundary | PASS/FAIL/UNPROVEN | [domain/service/repository/policy/contract proof] | ... |
| Correct seam | PASS/FAIL/UNPROVEN | [test/enforcement seam] | ... |
| Standard work | PASS/FAIL/UNPROVEN | [existing pattern or named new standard] | ... |
| Recurrence guard | PASS/FAIL/UNPROVEN | [ratchet/falsification proof] | ... |
| Refactor requirement | FIX-NOW/FOLLOW-UP/NOT NEEDED | [classification evidence] | ... |
```

Rules:

- Any `FAIL` or `UNPROVEN` row in Root cause, Ownership, SRP/cohesion, Domain boundary, Correct seam, Standard work, or Recurrence guard blocks `PASS` and `CONDITIONAL PASS`.
- `FIX-NOW` blocks `PASS` and `CONDITIONAL PASS` unless the plan includes exact tasks, files/symbols, owner boundary, acceptance criteria, and verification for that refactor before or inside implementation.
- `FOLLOW-UP` is allowed only when the structural issue is outside the defect/recurrence path and the current plan has a proven recurrence guard.
- `NOT NEEDED` requires evidence that ownership, SRP, domain boundaries, and seams already pass.
- A route, UI component, worker wrapper, test, script, fixture, or one-off SQL block can verify or call an invariant; it cannot become the only owner of a business rule unless source evidence proves that layer is the correct owner.

#### Symptom-Patch Vetoes

Mark the plan `FAIL` when it:

- Adds local handling for a bad state but leaves the writer that creates the bad state unchanged.
- Moves business policy into route glue, UI handlers, worker wrappers, scripts, tests, or fixtures.
- Requires equivalent logic to be copied into sibling routes, jobs, pages, queries, services, or tests.
- Adds a fallback, catch block, default, retry, or guard that masks the symptom without proving the owner cannot recreate the defect.
- Defers owner extraction, seam creation, duplicate-writer deletion, or domain refactor needed to prevent recurrence.
- Treats a migration/backfill as the fix while runtime writers can still recreate the bad rows.
- Uses mock-only, migration-only, old-branch, or stale PR proof when runtime code, live schema, or current tests are available.

### Step 5: Enterprise Architecture Gate

Run a separate assessment against enterprise-grade standards. This is not optional — it's the baseline expectation.

**The plan must demonstrate deliberate thinking in each area:**

| Enterprise Dimension | What to Check | Red Flag If Missing |
|---------------------|---------------|-------------------|
| **Observability** | Logging, metrics, alerting, dashboards | "We'll add monitoring later" |
| **Scalability** | Load considerations, bottlenecks, growth path | No mention of volume/scale |
| **Data Integrity** | Transactions, idempotency, consistency guarantees | Happy-path only design |
| **Security** | Auth, input validation, tenant isolation, secrets | Security as afterthought |
| **Recoverability** | Rollback plan, data recovery, failure modes | No rollback strategy |
| **Auditability** | Change tracking, who-did-what, compliance trail | No audit consideration |
| **Operability** | Runbooks, manual overrides, feature flags, on-call | Requires developer intervention for ops tasks |
| **Testability** | Test strategy, coverage approach, CI integration | "We'll test manually" |
| **Migration Safety** | Backwards compatibility, zero-downtime, data backfill | Big-bang cutover |
| **Documentation** | API contracts, architecture decisions, onboarding | Tribal knowledge only |

**Enterprise grading:**
- **Enterprise-Ready**: All dimensions addressed with concrete specifics
- **Needs Hardening**: Core functionality solid but gaps in 1-3 dimensions
- **Vibe-Coded**: Multiple dimensions missing or hand-waved — send back to planning

**Grading discipline — avoid the "current scale" excuse:**

A common rationalization is marking Scalability as "pass" because "we only have 71 suppliers" or "current volume is low." Enterprise-grade means the architecture can handle 10x growth without redesign. Don't grade against today's numbers — grade against where the system needs to be in 12-18 months. If the plan doesn't mention growth considerations at all, that's a gap, not a pass.

Similarly, don't give Observability a pass just because logging exists. Enterprise observability means: if this breaks at 2am, can the on-call engineer diagnose it without reading the source code? If the answer is "they'd need to check the database directly," that's a gap.

**The "we'll add it later" red flag:**

Any plan that defers enterprise dimensions to a future phase is not enterprise-grade — it's vibe-coded with a TODO list. Monitoring, rollback, runbooks, and security are not Phase 2 features. They ship with Phase 1 or the plan fails the enterprise gate. The whole point of this gate is to prevent "ship now, harden later" thinking.

### Step 6: Synthesize Conflicts

Cross-reference stakeholder concerns, the root-cause structural gate, and the enterprise gate:

- Where do stakeholder needs clash? (e.g., "faster for ops" vs "more audit trail for compliance")
- Where does the structural gate expose a symptom patch, wrong owner, duplicate rule, missing seam, or fix-now refactor?
- Where does the enterprise gate expose gaps no stakeholder caught?
- Where are concerns duplicated across perspectives? (signals a fundamental issue)

### Step 7: Produce the Audit Document

Output a structured document with this format:

```markdown
# 360 Audit: [Plan Name]

**Date:** [date]
**Document audited:** [path]
**Overall verdict:** PASS / CONDITIONAL PASS / FAIL

## Stakeholder Matrix

| Stakeholder | Concerns Found | Blockers | Highest Severity |
|-------------|---------------|----------|-----------------|
| [role]      | [count]       | [count]  | [BLOCKER/HIGH/etc] |

## Enterprise Architecture Grade

**Grade:** Enterprise-Ready / Needs Hardening / Vibe-Coded

| Dimension | Status | Detail |
|-----------|--------|--------|
| Observability | [pass/gap/missing] | [specific assessment] |
| ... | ... | ... |

## Root-Cause Structural Grade

**Grade:** Root-Cause Ready / Structurally Incomplete / Symptom Patch

## Evidence Ledger

| ID | Claim | Evidence | Source/command | Result |
|---|---|---|---|---|
| E1 | [claim] | [plan section, file:line, command output, schema/runtime proof] | [read/run/query/action] | PROVEN/CONTRADICTED/UNPROVEN |

## Assumption Ledger

| ID | Assumption | Evidence check | Status |
|---|---|---|---|
| A1 | [assumption] | [evidence ID or missing proof] | PROVEN/CONTRADICTED/UNPROVEN |

## Causal Chain

Symptom/outcome: [observed failure or desired workflow change] ([evidence])
  caused by: [immediate behavior] ([evidence])
    caused by: [missing/incorrect invariant, seam, owner, lifecycle, or contract] ([evidence])
      ROOT: [source invariant or ownership failure] ([evidence])

## Boundary Ledger

| Invariant / rule | Correct owner | Active entry points | Allowed writers | Allowed consumers | Boundary contract | Forbidden non-owner layers | Result |
|---|---|---|---|---|---|---|---|
| [rule] | [domain/service/repository/policy/schema/contract] | [routes/jobs/UI/scripts/webhooks] | [writer paths] | [consumer paths] | [method/schema/event/DTO/queue/repository route] | [layers that must not own/copy rule] | PASS/FAIL/UNPROVEN |

## Structural Checks

| Check | Result | Evidence | Required action |
|---|---|---|---|
| Root cause | PASS/FAIL/UNPROVEN | [plan section + source/runtime proof] | ... |
| Ownership | PASS/FAIL/UNPROVEN | [owner + callers/writers/consumers] | ... |
| SRP/cohesion | PASS/FAIL/UNPROVEN | [touched units + responsibilities] | ... |
| Domain boundary | PASS/FAIL/UNPROVEN | [domain/service/repository/policy/contract proof] | ... |
| Correct seam | PASS/FAIL/UNPROVEN | [test/enforcement seam] | ... |
| Standard work | PASS/FAIL/UNPROVEN | [existing pattern or named new standard] | ... |
| Recurrence guard | PASS/FAIL/UNPROVEN | [ratchet/falsification proof] | ... |
| Refactor requirement | FIX-NOW/FOLLOW-UP/NOT NEEDED | [classification evidence] | ... |

## Falsification & Recurrence Guard

[Old symptom proof target, adjacent/sibling proof target, entry-point coverage, and ratchet that fails if recurrence returns]

## Stakeholder Detail

### [Stakeholder Role]
| # | Concern | Severity | Mitigation |
|---|---------|----------|------------|
| 1 | [specific issue] | [level] | [suggested fix] |

## Conflicts & Tradeoffs

| Conflict | Stakeholders | Resolution Options |
|----------|-------------|-------------------|
| [description] | [who vs who] | [options] |

## Blockers (Must Resolve Before Implementation)

1. [blocker with clear description and owner]

## Recommendations

1. [ordered by priority]

## Verdict Rationale

[Why this plan passed/failed the gate, and what must change for conditional passes]
```

### Step 8: Gate Decision

- **PASS**: No blockers, enterprise-grade, stakeholder concerns addressed or explicitly accepted as tradeoffs, Root-Cause Structural Grade is `Root-Cause Ready`, every Boundary Ledger row is `PASS`, and no structural check has `FAIL`, `UNPROVEN`, or unresolved `FIX-NOW`.
- **CONDITIONAL PASS**: No blockers and no symptom-patch vetoes, but non-critical gaps exist outside the root-cause/recurrence path. List specific conditions that must be met before implementation, then require the audit to be re-run. Do not use CONDITIONAL PASS to defer root cause, ownership, SRP, domain boundary, seam, recurrence guard, or `FIX-NOW` refactor work.
- **FAIL**: Blockers present, enterprise grade is `Vibe-Coded`, Root-Cause Structural Grade is `Structurally Incomplete` or `Symptom Patch`, any Boundary Ledger row is `FAIL`/`UNPROVEN`, a structural check fails on the defect path, or required evidence is missing.

A CONDITIONAL PASS requires the conditions to be resolved and the audit re-run before proceeding. Don't let conditions become "we'll do it later" — that's how enterprise standards erode.

Before emitting a PASS, run this self-check:

- `ROOT_CAUSE_READY`: causal chain reaches the source invariant or ownership failure with evidence.
- `BOUNDARY_LEDGER_COMPLETE`: all eight required Boundary Ledger columns are present and every row is `PASS`.
- `FIX_NOW_CLOSED`: every `FIX-NOW` refactor is included in the implementation plan with exact files/symbols, owner boundary, acceptance criteria, and verification.
- `NO_CONSUMER_PATCH`: no route/UI/worker/script/test-only layer owns a business invariant unless it is source-proven as the owner.
- `RECURRENCE_RATCHET`: the plan names the guard that fails if the same defect class returns.
- `FALSIFICATION_READY`: active entry points and sibling flows have proof targets, not just happy-path tests.
- `EVIDENCE_FRESH`: required plan/code/schema/runtime claims were verified against the current checkout/runtime.
- `ASSUMPTIONS_PROVEN`: every assumption needed for root cause, ownership, SRP, domain boundary, seam, recurrence, rollout, and stakeholder impact is `PROVEN`.

## Common Mistakes

- **Fixed stakeholder list**: Don't audit every plan from 7 perspectives. A database migration doesn't need customer UX review. Derive stakeholders from the plan.
- **Generic concerns**: "Security could be an issue" is useless. "The plan doesn't specify how tenant isolation is maintained during the batch migration" is useful.
- **Skipping the enterprise gate**: Stakeholder review alone misses architectural gaps. The enterprise gate catches systemic issues.
- **Rubber-stamping**: If everything passes easily, the audit wasn't rigorous enough. Push harder on assumptions.
- **Over-auditing trivial changes**: A one-line config change doesn't need 6 stakeholder reviews. Scale the audit to the plan's blast radius.
- **Developer-heavy bias**: Technical reviews naturally gravitate toward developer concerns. If your audit has 7 developer issues and 1-2 per other stakeholder, you haven't pushed hard enough on non-technical perspectives. The whole point of 360 is to catch what the technical review misses.
- **Ignoring downstream data consumers**: Changing a timestamp's meaning, a status value's definition, or a calculation formula can silently break every report, dashboard, and export that uses that data. Always trace data changes downstream to their consumers.
- **Passing scalability because "current load is low"**: Enterprise-grade means the architecture handles growth without redesign. Grade against 10x, not today.
- **Missing the incremental delivery question**: Large plans that deliver zero value until 100% complete are a business risk. The strategic stakeholder should always ask: "Can we ship partial value earlier?"
- **Ungrounded concerns**: Every concern must cite a specific plan section, quote, or file. "Security could be an issue" is useless. "The plan encrypts credentials in migration 352 but never NULLs the plaintext column before the DROP in migration 353" is useful. If you can't anchor it, cut it.
- **Reviewing the plan without reading the code**: Plans contain claims about the codebase — file counts, existing services, table schemas, function behavior. These claims are frequently wrong. If you audit a code-related plan without verifying its claims against the actual source files, you're reviewing fiction. The most valuable findings in any audit are the gaps between what the plan says and what the code actually does.
- **Passing a symptom patch**: A plan that catches, formats, backfills, retries, or hides a bad state can still fail if the owner keeps creating the same state. Approval requires a source-owner fix and a recurrence guard.
- **Deferring fix-now refactors**: SRP, domain, seam, and ownership refactors are not polish when they sit on the defect path. They must be in the plan before implementation starts.
- **Letting conditional pass become approval**: Conditions are not permission to code through unresolved root cause, boundary, or recurrence gaps. Re-run the audit after conditions are resolved.
