---
name: recover-semantic-model
description: Recover a program's minimal semantic model (the state that changes what users see, how its transitions repeat and reorder, what each effect requires). Use when asked to recover or audit that model, to check what is idempotent or order-dependent, or to split a refactor into provably equivalent and "trust me" changes.
---

# Recover the semantic model

Recover the program's minimal semantic model: the smallest description of
its state, transitions and dependencies that predicts what its users
observe. Every finding points at a row of the model; one that names no row
is ordinary code review.

Stay read-only unless asked: no edits, tests or tickets. By default build
the three tables and run the four passes; split refactors when the request
mentions them or names a diff. Asked for one part, do that part and the rows
it needs. Read the [report layout](references/report.md) before the first
table: its worked example shows how full each cell should be.

## Scope and screen

Use the scope the user gave; with several programs and no hint, ask which.
Report what you modelled, what you skipped and the revision you read.

The screen is where a person, or a system acting for them, observes the
program: what a UI renders; a service's responses, messages, records other
programs read and money it moves; a library's returns, throws and callbacks.

Number rows S1, T1, E1, one row per stored copy of a fact, not per
variable. On a large scope, model one lifecycle or component at a time (a
job, a document, a family of consumers), main flows first, and list the rest
as not modelled.

## 1. State: every value that changes what the user sees

Stored fields, in-memory and client state, values held by another system (a
queue, a cache, a workflow engine), configuration that selects behaviour.

| ID | Value | Lives in | Writers | Readers on the way to the screen | Source, or copy of |
| -- | ----- | -------- | ------- | -------------------------------- | ------------------ |

- **Writers**: `path:line` or a T row; outside the repository, `unknown`.
- **Copy of**: the row restates another, like a counter beside the rows it
  counts, a cached status or a field repeated in a message.
- A value nothing reads stays, with `unobserved` as its readers.

## 2. Transitions: what commutes, what's idempotent, what's order-dependent

Every event that writes a state row or fires an effect: a user action, a
request, a delivered message, a timer, a retry, a recovery job. Cite the line
behind each classification.

| ID | Event | Writes | Guard | Applied twice | Against other transitions |
| -- | ----- | ------ | ----- | ------------- | ------------------------- |

- **Idempotent**: applied twice, same state and no new effect.
- **Commutes**: same state and effects in either order, interleaved included;
  a read then a write commutes only if the two are atomic.
- **Order-dependent**: name what makes each side atomic from check to write
  (a lock, a conditional write, a transaction whose isolation covers its
  read, or nothing) and what picks the order (a sequence number, an
  `await`, or nothing). A lock excludes; it does not pick.

Classify only pairs that can land in both orders and touch the same rows,
the same reader or each other's preconditions; requests sent in order can
still land out of order. Write `unknown` rather than guess; it is a coverage
gap, not a finding.

## 3. Dependencies: what must be true before each effect fires

An effect leaves the program or reaches the screen: a response, a rendered
value, a message, a charge, a call to another system. One row per
precondition (E1a, E1b).

| ID | Effect | Fired by | Must be true before | Enforcer |
| -- | ------ | -------- | ------------------- | -------- |

The enforcer is **here** (a check, constraint, transaction or type, with
`path:line`; a check against a copy is only as good as the copy),
**elsewhere** (a named caller, database, broker or service, with where the
guarantee is stated, or `unverified`), or **none found** (with where you
searched).

## Then find

The model is done when every S row names its writers, its readers (or
`unobserved`) and its source or the row it copies, every T row classifies
its repeat and its pairs (or `unknown`) and every E row names its enforcer.
Then run all four passes; a candidate becomes a finding only after
[Check each finding](#check-each-finding).

- **Nondeterminism in awaits, retries and event order.** For each queue,
  retry loop, webhook or scheduler, first state the intended delivery (at
  most or at least once, ordered or not, bounded or not) with the line that
  shows it; if nothing says, mark it `unstated`, list it under Decisions
  for the owner and continue. A candidate is a repeat meeting a cell that
  is not idempotent; two unordered events meeting a transition that is not
  atomic, or a pair whose order nothing picks and one outcome is wrong; or
  an `await` between an enforcer's check and its effect.
- **Invariants enforced by hope.** A precondition whose enforcer is **none
  found**, reported with your search. **Elsewhere** is a contract: record
  what the user sees if it changes.
- **One fact stored in two places, drifting.** For each copy row, list the
  writers of both. They drift when a writer updates one outside the other's
  atomic step, a retry repeats one write, or their lifetimes differ. Say
  which is the source, which the screen reads, which guards an effect.
- **Work that never reaches the screen.** `unobserved` rows, discarded
  results, swallowed errors, paid work repeated although its first result
  was kept. Give the cost. No reader here may mean a reader elsewhere: a
  contract question.

## Check each finding

Candidates fail when the code was misread, an enforcer already covers the
case, or two share a root cause. Before reporting one:

1. **Anchor it** to the S, T and E rows it violates.
2. **Give its smallest breaking input** (below). Unobserved work gives the
   reader search and the cost instead; a latent invariant gives the
   assumption and the change that would break it.
3. **Try to disprove it.** Read each cited line literally: a `try` around
   `return send()` catches nothing from the unawaited promise. Look along
   the writers and guards of its rows for a check that rejects a step, then
   try other routes to the same rows. If this program rejects them all, drop
   it as ruled out with the `path:line`; if only another system does, record
   the contract.
4. **Merge by root cause**: inputs that break at the same row and step are
   one finding with several symptoms. Link findings whose fixes interact.

### Smallest breaking input

A numbered event sequence from a named state to a wrong result on the
screen, as `start:`, steps, `seen:` and `expected:` (see F1 in the
[worked example](references/report.md#worked-example)).

- Each step is something a test can drive: a call, a delivered message, a
  killed process, a clock advance, a stored row. Prose is not an input.
- Removing any step removes the failure. One entity, two parties unless a
  third is needed.
- Each step cites its `path:line`; a comment or unread code makes it
  `unverified`. The count (`4/4 steps cited`) is the evidence level.
- If you cannot build one, name the assumption instead. Never invent one.

## Last, split my refactors into "provably equivalent" and "trust me"

Take the diff given; without one, the current branch against the default
branch, uncommitted changes included, and say so. If empty, report the split
as not covered. A change described as altering behaviour is not a refactor;
list it apart.

- **Provably equivalent**: no row, effect result or effect order changes for
  any input, and the argument fits in a line: a rename, a move, an
  extraction keeping calls and order, a reordering the transition table
  shows commutes. Passing tests are evidence, not the argument.
- **Trust me**: anything else, notably an `await` added, removed or moved, a
  shifted transaction boundary, error handling moved across a call, a
  changed default, predicate or serialisation, anything near retries or
  acknowledgement.

For each "trust me", give the smallest input that breaks it, with the old
result and the new, or `no breaking input found` and the assumption. One
that breaks is a finding, reported once, here.

## Report

Write in the user's language, following the
[report layout](references/report.md). The report describes one revision:
before implementing a finding, replay its input against the current code.

## Related skills

When one is not installed, don't reproduce its method: list the hand-off as
not covered with the install command.

- `find-implicit-state-machines`: reachable states of a lifecycle row, and
  ownership, persistence and recovery of queues, workers, leases and
  workflows; their delivery, idempotency and effect preconditions stay in
  this model. Keep this report's layout.
  `npx skills add kr4chinin/skills --skill find-implicit-state-machines`
- `convert-state-machines-to-actors`: the fix when several writers of one
  persisted state must go behind one owner. It edits code: run it only when
  asked.
  `npx skills add kr4chinin/skills --skill convert-state-machines-to-actors`
