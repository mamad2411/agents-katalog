---
name: estimation-and-slicing
description: Teaches relative sizing (S/M/L or points), slicing strategies to keep issues small, when to demand a spike instead of estimating, and how to flag oversized issues for splitting before development. Use when sizing issues or deciding whether an issue is small enough to build.
---

# Estimation and Slicing

Your job here is not to predict hours — it is to keep issues small enough to build, review, and verify safely, and to flag the ones that aren't. An estimate is a communication tool, not a commitment clock.

## Relative sizing

Size by comparison to known work, not in hours. Use one scale consistently:

- **T-shirt: S / M / L** — good default. S = a well-understood change touching one area; M = a story with a couple of moving parts; L = a story at the edge of one iteration.
- **Points (1, 2, 3, 5, 8)** — if the team already uses them. Same idea: relative effort + uncertainty, not time.

Sizing captures **effort and uncertainty together**. A tiny change in a scary, unfamiliar area is not an S. If two people size the same issue very differently, that gap is information — talk about *why* before averaging; the disagreement usually reveals a hidden assumption or missing acceptance criterion.

## Slicing strategies

Keep issues at S–M. Slice larger ones vertically (each slice ships observable value):

- **By workflow step** — split a flow into its stages; ship and verify each.
- **By data variation** — handle the common/simple input first, then the variants (saved card → new card → gift code). Each variant is its own slice.
- **Walking skeleton first** — build the thinnest end-to-end path that touches every layer, prove it works, then thicken. This retires integration risk early and gives QA something real to test fast.

Avoid horizontal slices ("all the backend," "all the UI") — they can't be demoed or QA'd independently and hide integration risk until the end.

## When to demand a spike instead of estimating

If you cannot size an issue because the *approach* is unknown, do not guess a number. Write a **spike** (set `type=spike`): a timeboxed investigation whose only deliverable is knowledge — a recommendation, a prototype, or the information needed to size the real work. Demand a spike when:

- The team can't agree on rough size because the unknowns dominate.
- The work depends on an unproven library, API, or integration nobody has tried.
- The right approach is itself an open architectural question (route it through the `human-approval-gate` — a spike can precede an ADR).

A spike is timeboxed and ends with a written finding, not shipped feature code.

## Flag oversized issues before development

Any issue sized **> L** (or above your team's agreed points ceiling) is too big to enter development. When you see one:

1. Comment that it exceeds the size ceiling and why.
2. Propose a split into S–M slices using a strategy above, or propose a spike if the size is unknowable.
3. Keep it out of `Todo` until it's sliced or a spike is scheduled.

A too-big issue is a review-and-QA hazard: large PRs get shallow reviews, and sprawling acceptance criteria get partially verified. Splitting is cheaper than the bug that slips through a rushed review of an L+ change.

## Quick reference

| Situation | Action |
|---|---|
| Clear approach, fits an iteration | Size S/M/L, proceed |
| Approach clear but too big | Slice vertically into S–M |
| Approach unknown, can't size | Write a `spike` |
| Sizing needs an architectural call | Route to the gate (`human-approval-gate`), possibly via a spike |
| Sized > L | Block from development, split first |
