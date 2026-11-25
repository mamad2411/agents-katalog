---
name: design-doc-writing
description: Drafts a design doc with goals, non-goals, alternatives considered and a rollout plan, grounded in the current code before proposing anything.
---

# Design doc writing

A design doc is a decision record, not a sales pitch. Make the trade-offs visible.

## Steps

1. Restate the problem in two sentences with who is affected and the evidence it is real (an incident, a metric, a support count). Ask the user for anything you cannot find.
2. Read the current implementation of the area. Summarize how it works today with file references; do not propose from assumptions.
3. Write **Goals** and **Non-goals**. Non-goals must be things a reader might reasonably expect, such as "no migration of historical data".
4. Write **Proposal**: the design in enough detail to estimate it. Cover data model, interfaces, failure modes, security and privacy impact, and effect on performance and cost.
5. Write **Alternatives considered**: at least two real options, including "do nothing", each with the reason it lost.
6. Write **Rollout**: phases, feature flag, migration steps, how to measure success, the rollback trigger and the rollback steps.
7. Close with **Open questions** and **Risks**, each with an owner or a way to resolve it.

## Rules

- Quantify where possible (requests per second, rows, latency, cost).
- Keep it to 2 to 4 pages; move detail into an appendix.
- Do not hide a weakness; state it and say how you would handle it.
- Never mark a question as resolved without evidence.

## Report

The doc path, the decisions you need from the user, and the claims you could not verify.
