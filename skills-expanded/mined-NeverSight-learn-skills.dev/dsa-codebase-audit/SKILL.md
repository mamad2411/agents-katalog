---
name: dsa-codebase-audit
description: Audit a whole codebase for material simplifications in data structures, state, algorithms, control flow, and ownership.
disable-model-invocation: true
---

# DSA Codebase Audit

Run an application-wide, read-only data-structures-and-algorithms audit. Find a small number of material simplifications in representation and organizing model—not cosmetic refactors.

## Audit boundary

The reviewed repository must remain unchanged. Inspect with read-only commands only. Do not edit files, generate patches, run tests, install dependencies, invoke formatters or generators, implement recommendations, commit, or push. Review existing tests as source evidence without executing them.

Use fresh read-only subagents when the runtime provides them. Give each worker one non-overlapping subsystem. Keep concurrency within the number of lanes you can actively coordinate. If fresh agents are unavailable, review one subsystem at a time in the coordinator context and disclose that limitation.

Maintain one canonical audit ledger in the coordinator context. It owns the subsystem inventory, statuses, accepted findings, explicit skips, cross-cutting patterns, duplicate or superseded findings, priorities, dependencies, and audit log. Worker reports are evidence for the ledger, never competing sources of truth.

The audit ends only after every inventory row is complete and the final audit has passed independent validation.

## 1. Establish the coverage contract

Inspect the repository root, project guidance, directory structure, manifests, entry points, public interfaces, dependency boundaries, and test layout. Inventory every identifiable subsystem before opening review lanes.

Include frontend, backend, shared infrastructure, platform bridges, generated-contract ownership, and test or tooling infrastructure wherever materially relevant. Give each subsystem:

- a stable ID and descriptive name;
- an exact, non-overlapping ownership boundary;
- key implementation files;
- relevant public interfaces, major call sites, and tests;
- one status: `queued`, `in-review`, `recommend`, or `skip`.

A broad catch-all row does not prove coverage. Split it until a worker can inspect the owned behavior and its callers without taking responsibility for another row.

Complete this step when every relevant source and test area maps to exactly one auditable subsystem, boundaries do not overlap, and the canonical ledger contains every row.

## 2. Run bounded subsystem reviews

Allocate each `queued` row to one fresh worker and mark it `in-review` before dispatch. Never give one worker multiple subsystems. Run independent rows concurrently only when their boundaries are distinct; otherwise run them sequentially. Use one consolidated wait for each batch, let productive workers finish, and harvest every usable result before opening replacement lanes.

Give each worker this brief, filled with its assigned row:

```markdown
Review subsystem <stable ID and name> for at most two materially useful simplifications in its data structures, state representation, control flow, algorithms, or organizing model.

Boundary: <exact owned files and behavior>
Key files: <paths>
Interfaces, callers, and tests to inspect: <paths or symbols>

This is read-only. Inspect the implementation, public interfaces, major call sites, and existing tests. Stay inside the assigned ownership boundary. Name cross-subsystem concerns, but do not expand scope to solve them.

Look for:
- scattered booleans or nullable fields that permit invalid combinations and should become a state machine or discriminated union;
- repeated assumptions about object shape that need one shared typed model;
- duplicated branching that a small map, registry, reducer, transition table, or command model would remove;
- unclear state or behavior ownership that a small module boundary would clarify;
- repeated scans, transformations, or lookups where a more appropriate collection or index materially simplifies behavior;
- lifecycle, concurrency, or async representations that permit stale or contradictory state.

Prefer clear local code when it is already sufficient. A recommendation must remove material complexity rather than move existing branching behind a new type. Exclude changes justified only by stylistic consistency, hypothetical extensibility, or minor line-count reduction.

Return at most two opportunities. Return `skip` when none clears that threshold.

For each opportunity provide:
1. Verdict: `recommend` or `skip`.
2. Evidence with exact file and line references.
3. Current complexity or invalid states.
4. Proposed representation and why it is simpler.
5. Smallest credible implementation scope, including affected files and interfaces.
6. Regression risks and migration concerns.
7. Existing and additional validation required.
8. Confidence: `high`, `medium`, or `low`.
```

A failed or missing worker leaves its row incomplete; it is not a skip. Re-run that row in a fresh lane or review it sequentially.

Complete this step when every row has a usable report containing one or two schema-complete candidates or an explicit `skip`.

## 3. Verify and synthesize

Independently trace every candidate through the current implementation, callers, public contracts, and tests before accepting it. Confirm each cited line and the claimed invalid state, duplication, ownership problem, or algorithmic cost.

Reject, narrow, or demote a candidate when it:

- is vague or lacks source evidence;
- duplicates another finding;
- misunderstands intentional semantics;
- merely relocates complexity;
- introduces a broader abstraction than the demonstrated need;
- relies on hypothetical scale or extensibility;
- falls outside its subsystem boundary.

Deduplicate by root cause. Assign every accepted recommendation to one authoritative subsystem, and record related rows as covered rather than repeating the finding. Record a verified no-finding result as an explicit skip. Update each row to `recommend` or `skip` only after coordinator verification.

Continue opening bounded batches until no row remains `queued` or `in-review`.

Complete this step when every inventory row has a verified disposition and every accepted finding has all eight required fields.

## 4. Audit the audit

Run fresh independent read-only passes, using separate agents when available, for:

1. repository coverage and missing subsystem boundaries;
2. duplicate findings and ownership overlap;
3. materiality and over-abstraction;
4. finding-schema completeness;
5. dependency-aware priority ranking.

If the coverage pass finds a real omission, add a new explicit subsystem row and audit it. Preserve completed boundaries rather than hiding the omission by broadening a prior row. Resolve every other validation failure in the ledger before reporting.

Rank accepted recommendations by concrete impact, confidence, implementation effort, blast radius, prerequisites, and ordering dependencies. Identify the best first implementation slices; do not implement them.

Complete this step when all five passes have a recorded result, every defect they found is resolved or disclosed, and the repository remains unchanged.

## 5. Report

Return one report with these sections, in order:

```markdown
## Summary
<Scope, recommendation count, skip count, and strongest themes.>

## Coverage
| ID | Subsystem | Ownership boundary | Key files | Public interfaces and major call sites | Tests | Disposition |
| --- | --- | --- | --- | --- | --- | --- |

## Prioritized recommendations
### 1. <Concrete simplification> — <confidence>
- **Verdict:** `recommend`
- **Subsystem:** <ID and name>
- **Evidence:** `path:lines`, ...
- **Current complexity:** <complexity or invalid states>
- **Proposed representation:** <model and why it is simpler>
- **Smallest scope:** <affected files and interfaces>
- **Risks:** <regression and migration concerns>
- **Validation:** <existing and additional validation required>
- **Priority:** <impact, effort, blast radius, prerequisites, and dependencies>

## Cross-cutting patterns
<Patterns observed across authoritative subsystem findings.>

## Explicit skips
<Subsystems with a concise verified reason no recommendation cleared the bar.>

## Audit validation
<Results of the five independent passes, worker failures or limitations, and confirmation that the repository remained unchanged.>
```

The audit is complete only when every identifiable subsystem appears in Coverage; every row ends in a recommendation or explicit skip; every finding has exact evidence, scope, risk, and validation; duplicates and weak abstractions are absent; priorities and dependencies agree; all five validation passes are accounted for; and the reviewed repository remains unchanged.
