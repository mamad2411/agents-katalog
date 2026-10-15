---
name: test-scenario-design
category: qa
description: Use while deriving cases - Given/When/Then and the techniques (partitions, boundaries, decision tables, state transitions) that find the cases the criteria do not state
---
# Test Case Design

Write each case as Given (preconditions), When (action via the real endpoint or UI), Then (the observable result). The Then is the `expected` field: state it before you run anything, or you will be judging the output against whatever it turns out to be.

## Two sources, in this order

1. **What was asked for.** At least one case per acceptance criterion, linked with `criterion_id`.
2. **What it implies.** The behaviour a reasonable person expects from the request even though nobody wrote it down. These are the cases with no `criterion_id`, and they are where defects actually live.

## Techniques for finding the implied cases

- **Equivalence partitioning:** group inputs into classes that should behave alike (valid email / invalid-format email / empty), then test one representative per class instead of guessing randomly.
- **Boundary value analysis, 3-value:** for every limit, test min−1, min, min+1, max−1, max, max+1 — off-by-one errors live exactly at these six points.
- **Decision table:** when a result depends on several conditions combined (role × state × flag), write the table and test the combinations that differ in outcome, not just each condition alone.
- **State transition:** model the valid states and the moves between them, then test the invalid moves too — cancel a completed item, edit after archive, submit twice.
- **Zero-One-Many / Some-None-All:** for anything list-shaped, test zero items, one item, many items; for anything that can apply to a set, test it applying to none, some, all.
- **Interrupt and repeat:** double-click a submit button, use the back button mid-flow, open the same record in two tabs, refresh mid-flow.
- **"Is this actually a bug?" oracles:** compare the observed behaviour against the product's own history (did it used to work differently), its own other screens (image), comparable products, the explicit claims in the task/docs, what a reasonable user would expect, the stated purpose of the feature, and plain consistency with itself — an oddity that fails none of these is a style choice, not a defect.

## Sources of "what the request implies"

The acceptance criteria, the human's comments, the analysis spec (`list_task_documents` — the behaviour statements are oracles, the implementation plan is not), and `list_links` (dependencies the change touches imply side-effect and failure cases).

## Rejecting a case

Rejecting a case is a result, not a deletion. When you work one out and decide it does not apply, record it with `status=invalid` and say why in `notes`. The three reasons that recur: it contradicts the stated spec, it is unreachable in this deployment, or it belongs to a different task. A reviewer reading your round has to be able to see that you considered it.

## Worked Example

"Users can rename a project (1-80 chars, unique per workspace)":

- Happy path: rename to a new unique 40-char name → 200, name updated (`happy_path`).
- Boundary: 1 char, 80 chars, 81 chars (`boundary` x3).
- Negative: empty string, whitespace-only, name already used in this workspace (`negative` x3).
- Auth: rename another workspace's project → 403 (`auth`).
- Empty state: rename the only project in an otherwise-empty workspace (`empty_state`).
- Regression: project list sort order still correct after rename (`regression`).
- Invalid, rejected: "rename while another user is renaming the same project" — `status=invalid`, "no optimistic-locking requirement in the spec, out of scope".
- Invalid, rejected: "rename via the public API" — `status=invalid`, "this endpoint is UI-only per the spec".

About 10-12 cases across categories, two of them `invalid` with reasons.

If an acceptance criterion cannot be tested as written: when there is a concrete choice between two readings, `ask_user` with the readings as options (qa-verify-before-verdict's blocker triage) and continue testing what you can meanwhile. When it is simply unclear in a way with no concrete reading to offer, reject it via `review_criterion` with "untestable as written: <why> — needs a sharper criterion" and let the move to need_revision surface it on the card — a comment asking the PM to sharpen it reaches nobody, since the PM is not subscribed to in_qa.
