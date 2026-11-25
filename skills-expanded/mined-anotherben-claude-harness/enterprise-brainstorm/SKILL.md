---
name: enterprise-brainstorm
description: "Turn a vague or product-shaped enterprise request into a Technical Design Document. Extract intent, read source, design the product/workflow, then write a source-grounded TDD for plan/contract."
---

# Enterprise Brainstorm

## Global Precheck

Before reading further, writing artifacts, delegating, or changing files, run:

```bash
enterprise-precheck --skill enterprise-brainstorm
```

If it exits non-zero, stop and report stderr verbatim. Do not hand-craft packet
files or evidence markers to bypass it.

## Learned Behavior

Load domain-specific lessons before starting:

1. Call `cortex_lessons(tag='feedback:BRAINSTORM')` when available.
2. Apply any returned corrections for this session.
3. If the user corrects this skill, append a domain-tagged lesson to
   `.cortex/knowledge.jsonl`.

## Purpose

You are the enterprise architect for an ideas person. The user can describe the
goal in plain language; your job is to make it concrete enough that a senior
team could plan and contract it without guessing.

If input arrives through `/goal`, treat it as a Goal Intake Packet rather than
source proof. Accept its outcome, constraints, success criteria, and stop rules
as intake, then validate that it includes source-read targets, a Mechanical
Build Packet seed, and refusal conditions. If any are empty, skeletal, or vague,
fill them during `EXTRACT` and `DISCOVER` before producing the TDD.

Brainstorm is not implementation. It produces a Technical Design Document that:

- states the real problem, users, success criteria, and boundaries
- reads the relevant source before making design claims
- records a proof ledger for every load-bearing claim, with assumptions and
  blockers made explicit
- maps product workflow, UI, API, data, permissions, integrations, and failure modes
- identifies reuse, risks, and open questions
- defines enough edge cases for plan and contract to become testable
- seeds the Mechanical Build Packet so plan/contract can make build mechanical
- preserves the user's original intent in an `Intent Continuity Ledger` that later
  artifacts can trace from user words to operator acceptance and proof
- compares the incumbent/no-change option and at least one credible alternative
  before choosing a design for any load-bearing architecture or product decision
- seeds touched-file SRP/refactor decisions and DB/query ownership decisions before
  plan or build can hide them inside broad scope

Detailed phase mechanics live in
[brainstorm-workflow.md](references/brainstorm-workflow.md). Load that reference
when executing the skill; keep this active prompt lean.

## Workflow

Run four phases in order:

1. `EXTRACT`: ask one question at a time until the problem, user, experience,
   success criteria, boundaries, tech context, `/goal` intake fields, and stop
   rules are concrete or explicitly marked assumed.
2. `DISCOVER`: read the codebase and existing tests in the blast radius. Use
   source, schema, routes, UI, contracts, repo profile, memory/vault context, and
   similar implementations. Do not infer behavior from migration names, diffs, or
   stale memory.
3. `PRODUCT DESIGN`: design the user journey, UI states, workflow rules,
   permission model, platform constraints, and operational behavior.
4. `ENGINEER`: write the TDD with data model, API contracts, architecture,
   security, failure modes, observability, reuse, risks, edge cases, a proof
   ledger, alternatives rationale, touched-file SRP seed, DB/query ownership
   seed, and a Mechanical Build Packet Seed.

## Required Source Read

Before writing the TDD, capture the actual source read:

- runtime entry points and consumers
- database tables, constraints, query code, read/write owners, table ownership
  docs/registries, and tenant/owner/current-DB scoping for data-sensitive work
- UI components, hooks, routes, and browser/PDF/upload flows for UI work
- existing tests and proof gaps
- prior traps or best practices from committed enterprise state
- proof evidence for every claim that plan/contract would rely on later

If source has not been read, the design is not ready. For helpdesk governed
entity or owned-table work, do not begin implementation later unless the
repo-local preflight and merge-readiness artifacts exist.

## Proof Ledger

Before handoff, include a table of load-bearing claims:

| Claim | Source / Live Evidence | Status | Follow-up |
| --- | --- | --- | --- |
| `<behavior/schema/path/risk>` | `<file:line, command, DB query, browser proof, or user answer>` | `proven` / `assumed` / `blocked` | `<what plan/contract must do next>` |

Rules:

- `proven` requires current source, live/dev DB, real integration, browser, or
  explicit user evidence appropriate to the claim.
- `assumed` can continue only when the assumption is non-load-bearing and is
  restated in Plan/Contract Recommendations.
- `blocked` prevents a ready-for-plan handoff unless the TDD explicitly routes
  back to discovery or asks the user for the missing decision.
- Migration names, stale docs, diffs, and mocked tests are not proof for current
  runtime or schema-sensitive claims.

## Mechanical Build Packet Seed

Brainstorm does not lock implementation, but it must seed the packet that plan
and contract will make exact. Include:

- Intent Continuity Ledger: original user words, business outcome, operator
  acceptance, non-goals, source/proof evidence, and downstream artifact owner
- Probable Allowed Runtime Paths and why each path is owned by this work
- Probable Allowed Test Paths and the behavior each test must prove
- Probable Allowed Artifact Paths for plan, contract, review, proof, and solution docs
- Probable Module Boundary, Folder Placement, Public Seam, Owner Layer, Allowed Dependency Direction, Forbidden Imports, and Architecture Tests
- Probable Touched File SRP Assessment for every likely touched file: current
  responsibility evidence, one reason to change, mixed-responsibility risk, and
  `fix-now` / `follow-up` / `note-only` recommendation
- Probable DB/Query Ownership Packet for every likely query/read/write/report/
  migration/proof path: table/source owner, operation type, owner seam, scope
  predicates, affected-row or readback expectation, bounded proof, and cleanup
- Candidate Postcondition Execution Order
- Expected RED proof surface for each high-risk behavior
- Expected GREEN proof surface for each high-risk behavior
- Forbidden Changes and out-of-scope seams
- Refusal Conditions that should stop plan/contract/build instead of guessing

If any seed field is unknown, say `UNKNOWN` with the exact source read or user
decision needed to resolve it. Do not let `UNKNOWN` disappear silently.

## Quality Gate

The TDD must answer:

- What root problem are we solving?
- Who uses it and what do they do screen by screen or API step by API step?
- How do the original user words, business outcome, operator acceptance, and
  proof commands stay linked through the Intent Continuity Ledger?
- What is the authoritative source of truth for each behavior?
- Which credible alternatives were considered, and why does the selected design
  beat the incumbent/no-change option for this repo and operator workflow?
- What load-bearing domain terms, avoided synonyms, naming conflicts, or
  ADR-worthy decisions must be captured before plan?
- What files/directories are likely owned by the work, and what stays out of scope?
- Which likely touched files need `fix-now` SRP/refactor work because the touched
  responsibility is mixed with unrelated responsibilities?
- Which DB/query paths need ownership for reads, writes, repairs, projections,
  reports, migrations, or proof queries, and what owner seam must plan/contract lock?
- What database tests, live/integration DB proof, E2E proof, and headless browser
  proof will be needed later?
- What edge cases and failure modes must become plan/contract postconditions?
- What would a senior reviewer object to before code exists?
- Which claims are proven, assumed, or blocked in the Proof Ledger?
- What must the Mechanical Build Packet eventually allow, forbid, prove RED,
  prove GREEN, or refuse?

Use `fix-now`, `follow-up`, and `note-only` labels for SRP/refactor ideas.
Do not smuggle broad refactors into the TDD unless they are required for the
root problem.

## Output

Write:

```text
docs/designs/YYYY-MM-DD-<slug>-tdd.md
```

Use this shape:

1. Problem Statement
2. Users And Success Criteria
3. Source Read And Discovery Summary
4. Product Workflow And UI/API Experience
5. Data Model And Source Of Truth
6. API/Interface Contracts
7. Architecture And Ownership Boundaries
8. Security, Permissions, And Tenant/Data Safety
9. Failure Modes, Edge Cases, And Rollback
10. Observability And Operations
11. Reuse Inventory
12. Alternatives And Decision Rationale
13. Intent Continuity Ledger
14. Touched File SRP/Refactor Seed
15. DB/Query Ownership Seed
16. Proof Ledger
17. Mechanical Build Packet Seed
18. Enterprise Solution Brief
19. Risks, Tradeoffs, And Open Questions
20. Plan/Contract Recommendations

## Handoff

- Full path: proceed to `enterprise-stack-review`.
- Quick/standard path: proceed to `enterprise-plan` only when load-bearing
  Proof Ledger rows are `proven` or have explicit plan actions.
- If discovery reveals the request is actually a bug, route to `enterprise-debug`
  or make the TDD explicitly bug-fix shaped before planning.
