---
name: goal-lean
description: Execute a long-running objective with explicit completion criteria and bounded agents, reviews, retries, and scope. Use only when the user explicitly invokes /goal-lean with an objective.
argument-hint: <objective and optional completion criteria>
disable-model-invocation: true
---

# Lean Goal

Treat the following text as the outcome to complete:

$ARGUMENTS

## Operating contract

1. Extract the outcome, constraints, and observable completion criteria. Make reasonable assumptions for incidental details; ask only for a missing decision that materially changes the result.
2. Begin the work immediately with one capable agent and the relevant working tools. Do not return a process proposal instead of executing.
3. Add agents only for genuinely independent parallel work or unavailable expertise. Give each one a bounded deliverable and integrate its result once. Do not create leads, coordinators, or permanent reviewers by default.
4. Use no separate reviewer for low-risk reversible work. Use at most one bounded independent review for material correctness, security, safety, financial, legal, destructive, or production risk. Allow "no material issue" and never review a review.
5. Use deterministic tests and checks directly when they prove completion. Do not create benchmarks, reports, evaluation suites, or new skills unless they can change the current decision or completion status.
6. After two consecutive iterations without material improvement in the completion evidence, stop expanding the work. Present the current result, unresolved uncertainty, and smallest decision or input required.
7. Finish as soon as the observable completion criteria are satisfied. Do not continue with optional improvements that were not requested.

Treat agents, reviews, tests, reports, tool calls, and tokens as costs, not evidence of progress. End with the completed outcome or a precise blocker, never a proposal for another review cycle.
