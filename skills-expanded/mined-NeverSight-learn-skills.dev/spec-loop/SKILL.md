---
name: spec-loop
description: "Run the evidence-first Forge loop for a subject spec. Use this when you need to process evidence one unit at a time, produce unit summaries, rewrite the rolling summary, branch out to sub-agents for bounded exploration, choose adaptive clarification profiles, and emit speculative variants when blockers remain."
allowed-tools: Read, Write, Edit, Glob, Grep, Agent
---

Use this after intake and whenever more evidence work is needed.

## Core loop

For each evidence unit:
1. write a one-sentence `unit summary`
2. rewrite the one-sentence `rolling summary`
3. update claims and provenance links
4. update critical decision coverage and blocker state
5. if the evidence introduces or refines domain terms, update
   `UBIQUITOUS-LANGUAGE.md` at the project root
6. choose the next action:
   - `Read More`
   - `Ask`
   - `Mark Assumption`

## Hard rules

- Never append to the rolling summary mechanically. Rewrite it.
- Every canonical claim must be traceable through sidecar claim ids and
  evidence unit ids.
- If the evidence source is large, spawn sub-agents per independent area.
- Sub-agents return typed patch proposals only.
- No major canon claim may exist without `evidence_refs` or an explicit
  assumption id.
- Analogy prompts are ambiguity-heavy by default.
- `question_rounds_completed = 0` on a `sparse` `analogy_feature` or
  `parity_clone` run means required clarification buckets are still open unless
  the user explicitly approved a recommended default pack.

## Clarification policy

First classify or reuse `request_archetype`.

Use these clarification profiles:

- `feature`, `analogy_feature`, `parity_clone`
  - `core_outcome`
  - `scope_boundary`
  - `implementation_constraints`
  - `acceptance_signal`
- `bugfix`
  - reproduction
  - expected behavior
  - environment/version boundary
- `integration`
  - external system boundary
  - auth/data ownership
  - failure/retry expectations
- `migration`
  - source/target boundary
  - compatibility window
  - rollback expectation

Additional required categories by archetype:

| Category | feature | analogy_feature | parity_clone | integration | bugfix | migration | refactor | reverse_spec |
|----------|---------|----------------|-------------|-------------|--------|-----------|----------|-------------|
| Failure modes | required | required | required | required | required | required | optional | required |
| Security boundaries | required | required | required | required | optional | optional | optional | required |
| Edge cases | required | required | required | required | required | required | optional | required |
| Scalability assumptions | required | optional | optional | required | optional | required | optional | optional |
| Operational concerns | required | optional | optional | required | optional | required | optional | required |
| Ordering and concurrency | required | optional | optional | required | required | required | optional | optional |

Categories marked `required` must be addressed before the drafting gate opens.
Categories marked `optional` are skipped unless evidence suggests relevance.

Walk down each branch of the design tree. For each branch, determine whether
evidence closes it or whether ambiguity remains that blocks critical decision
coverage.

Ask only if:
- passive evidence is exhausted, ambiguous, or lower value
- the ambiguity blocks critical decision coverage or blocker closure

Ask the user directly when input is needed.
Ask one batch at a time, max `3`, with recommended options first.
Allow a recommended default pack when the user can approve defaults in one
reply.
Record answers as new `evidence_unit` records.

## Research-first directive

Walk down each branch of the design tree. Before escalating any question to
the user:
1. search the codebase for existing patterns, implementations, or conventions
   that answer it
2. check existing evidence and prior clarification answers for implicit answers
3. check `AGENTS.md` for prior implementation learnings that answer it
4. only escalate if genuinely unanswerable from available sources

For `sparse` `analogy_feature` or `parity_clone` runs:
- seed required clarification ids before drafting:
  - `rq-core-outcome`
  - `rq-scope-boundary`
  - `rq-implementation-constraints`
  - `rq-acceptance-signal`
- do not mark those buckets `covered` from analogy alone
- if the user does not answer, keep the run in
  `AWAITING_CLARIFICATION` or `SPECULATIVE_DRAFT`

## Raised drafting gate

All required categories (per archetype matrix) must be addressed before
transitioning to drafting. "Addressed" means the loop has a concrete answer
from evidence, codebase research, or user answer — or has explicitly marked the
category as out-of-scope with user agreement. "We didn't think to ask" is not
addressed.

## Escalation re-entry

When `adversarial-escalation.json` or `beads-escalation.json` is present as
input, scope the round to the escalated findings only. Do not run a full
generic pass. Address the specific findings, affected sections, and reopened
blockers listed in the escalation artifact. Both artifact types use the same
schema and are handled identically.

## Speculative mode

If required clarifications remain unresolved:
- do not collapse uncertainty into one canonized solution shape
- emit `2-3` bounded variants instead of one settled handoff path
- each variant must list:
  - included scope
  - excluded scope
  - unresolved decisions
  - tradeoffs
  - risk notes
- set `planning_status=SPECULATIVE_DRAFT`
- keep `handoff_status=WITHHELD`
- do not emit one canonized “best guess” subject spec as if it were final

## Required outputs

Update:
- `spec-ledger.md`
- `question-backlog.md`
- `evidence-ledger.jsonl`
- `claim-ledger.jsonl`
- the `Core Model`, `Behavior and Flows`, and `Open Questions` sections

`question-backlog.md` must always split:
- `Required Clarifications`
- `Deferred Questions`
- `Non-blocking Assumptions`

`No open planning-critical questions` is illegal for a `sparse`
`analogy_feature` or `parity_clone` run unless:
- each required clarification id is closed by evidence
- or answered by the user
- or explicitly approved through a recommended default pack

## Branching guidance

Good fanout targets:
- separate docs sections
- separate subsystems
- UI vs API behavior
- contradiction investigations

Bad fanout targets:
- tightly coupled edits to the same section
- final readiness decisions
- user interaction policy
