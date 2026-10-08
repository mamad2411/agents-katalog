# `log-skill` — Active Operator Command V0.2

**Status:** ACTIVE  
**Version:** 0.2.0  
**Owner:** Doc Reo

## Purpose

`log-skill` is the Active Signalproof operator shorthand for preserving and synchronizing milestone/learning state. It coordinates Closeout, Learn, Verify, Document, Handoff, Router, and the Signalproof Library architecture while preserving public/private evidence boundaries and Build Ledger chronology.

> **Logging does not reserve a canonical event number. Canonical chronology is assigned only by a verified chain-safe append.**

## Forms

### `log-skill`

Preserve/synchronize current milestone or learning state without claiming closure unless closure is established and authorized.

Required behavior:

- identify work unit and evidence state;
- deduplicate existing records where available;
- extract reusable learning under lifecycle governance;
- run the Skill Architecture Check when a Skill is created or materially changed;
- publish only public-safe records and preserve private evidence separately;
- stage when canonical append is unavailable/unnecessary/unauthorized;
- do not reserve a C-number or auto-activate a candidate.

### `log-skill close`

Request full immediate closeout for work that is actually complete.

Route:

`Validate -> Record -> Extract -> Govern -> Closeout -> Verify`

Before canonical append, verify actual ledger identity/head/chain/projection, deduplicate stable identities, use approved chain-safe tooling, and run native/original verification after append. Otherwise preserve a staged/noncanonical closeout.

### `log-skill close-when-complete`

Latch the current milestone as closure-required before phase transition while leaving it open. Preserve acceptance criteria; when complete, route through `log-skill close`. Never reserve a future sequence.

### `log-skill close C###`

Strict conditional close. The requested number is an assertion, never a reservation. Proceed only when verified canonical chronology makes it the next valid sequence and all normal gates pass; otherwise STOP.

## Skill Architecture Check

When the work creates or materially changes a `SKILL.md`:

1. measure exact UTF-8 bytes before and after where a prior version exists;
2. classify the new file using the Signalproof Skill Budget;
3. check responsibility cohesion and duplicate doctrine, not size alone;
4. prefer root inheritance, registries, loops, schemas, tests, policies, or separate routeable specialists over repeated prose;
5. at **12,000–14,999 bytes**, require decomposition/conciseness review before material expansion;
6. at **15,000+ bytes**, block promotion/material expansion until the Skill is refactored below the ceiling;
7. verify Router/registry/test effects of any split.

Record when applicable:

- `skill_bytes_before` / `skill_bytes_after`;
- budget status before/after;
- atomicity/decomposition decision;
- extracted/new Skill candidates;
- duplicate doctrine removed;
- routing changes;
- tests and protected behavior;
- supersession/rollback path.

A small Skill can still require decomposition if it contains independently routeable responsibilities. A large Skill must not be shortened by deleting required governance merely to satisfy the budget.

## Preview / Idempotency

Projected C-labels remain **PROJECTION / PREVIEW / NOT CANONICAL** until native append assigns them. Repeated `log-skill` verifies/synchronizes stable identities rather than creating duplicates.

## Public/private boundary

Public Signalproof-Skills may contain public-safe lessons, tests, governance records, and candidate changes. Private Build Ledger evidence may contain internal chronology, hashes, recovery, and staged closeout details. Never leak private ledger heads, local paths, credentials, customer/private data, or recovery internals publicly without authority.

## Lifecycle

Outputs are not automatically Active:

`DISCOVERED -> CANDIDATE -> TESTED -> APPROVED -> ACTIVE -> DEPRECATED / RETIRED`

## STOP conditions

STOP when chronology cannot be verified, a projection is treated as canonical, a duplicate would be appended, completion is falsely claimed, private evidence would leak publicly, an output is auto-promoted, a changed Skill violates the 15,000-byte ceiling, or command scope would expand into unauthorized canonical mutation.
