---
name: simple-simplify
description: >
  Audit a recent implementation diff for unnecessary complexity and propose behavior-preserving
  simplifications without changing code. Use after simple-implement or simple-run when the user
  asks to simplify, reduce complexity, remove overengineering, or review generated code for a
  smaller and clearer solution.
disable-model-invocation: true
---

# Simple Simplify — Audit an Implementation for Simplification

Review completed implementation work with one goal: find complexity the requirements do not need.
Produce proposals only. Do not edit code, project state, or documentation.

## Workflow

### 1. Establish the review scope

Use the first scope that applies:

1. A commit or range named by the user.
2. The current uncommitted diff after a task.
3. The contiguous feature commits identified by task IDs in `issues.json` and commit messages.

Confirm the scope contains only the intended work. If it is ambiguous or mixed with unrelated
changes, ask the user for a base ref or range before continuing.

### 2. Read the constraints

- Read repository instructions and conventions.
- Read the feature's spec, design, issues, and relevant progress entries when available.
- Read the diff, then inspect only the callers, tests, and surrounding code needed to understand it.

Treat requirements and public behavior as constraints. You may question a documented design choice,
but label any proposal that changes it as decision-required rather than behavior-preserving.

### 3. Audit for unnecessary complexity

Look for complexity introduced or made obsolete by the reviewed work:

- abstractions, layers, or files with no demonstrated need;
- speculative configurability, extension points, or generic APIs;
- duplicated logic or parallel representations of the same state;
- forwarding helpers and types that add indirection without policy;
- branches for states already made impossible by validated invariants;
- dependencies that replace a small, clear local implementation;
- obsolete code, fixtures, helpers, or configuration;
- tests whose setup is more complex than the behavior under test.

Do not optimize for fewer lines. Prefer fewer concepts, states, branches, dependencies, and places
that must change together. Ignore style preferences, unrelated pre-existing code, hypothetical
future cleanup, and reductions that weaken clarity, correctness, security, or test coverage.

### 4. Report proposals

Report only specific, evidence-backed simplifications. Rank them by expected benefit and separate:

- **Safe simplifications** — preserve documented behavior and can be verified directly.
- **Decision-required simplifications** — change architecture, public interfaces, or documented decisions.

For each proposal include:

- the affected files or symbols;
- evidence that the complexity is unnecessary;
- the concrete simpler approach;
- expected benefit and risk;
- how to verify behavior remains correct.

If no worthwhile simplification exists, say so clearly. A clean pass is a successful outcome. Do not
manufacture findings, write files, add tasks, or implement proposals.
