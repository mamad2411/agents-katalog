---
name: deep-optimize
description: Review every dimension for optimization opportunities with parallel subagents + prioritized plan
argument-hint: "[path-or-target] [--diff] [--apply]"
related:
  - deep-thinking
  - deep-review-codebase
  - use-subagents
  - follow-parallel
  - deep-analyze
  - implement-to-production
  - report
  - suggest-next-action

---

## Goal

Review every dimension of the codebase to find optimization opportunities using `/use-subagents` in parallel — performance, bundle, database, algorithm, dependencies, architecture, build, cost — then consolidate into a prioritized, evidence-backed optimization plan

## Scope

Use when you want to optimize across many dimensions at once — report-only by default; `--apply` fixes according to the plan after user confirm

- Compared with nearby skills: `/deep-review-codebase` = correctness/standard/report review; `/deep-optimize` = drill into specific bottlenecks; `deep-optimize` = fan out every dimension with subagents then merge the plan into prioritized actions
- `/ship` always calls this skill in the Validate step before merge/release

## Execute

### 1. Scope And Slice

> Goal: divide the target into dimension slices that can be reviewed independently

1. Accept `[path-or-target]` — unspecified = full repo; `--diff` = only files in `git diff`
2. Run `/scan-codebase` to identify hot paths, build outputs, manifests, data layer, UI layer
3. Split into dimension lanes (non-overlapping file ownership):

| Lane | Dimension | What to check |
|------|-----------|---------|
| 1 | `runtime` | hot paths, sync I/O, unnecessary awaits, re-renders, N+1 |
| 2 | `bundle` | bundle size, tree-shaking, chunks, static assets, sourcemaps |
| 3 | `data` | queries, indexes, caching, pagination, serialization |
| 4 | `algorithm` | time/space complexity on critical paths |
| 5 | `deps` | heavy/unused deps, polyfill bloat, update opportunities |
| 6 | `architecture` | layering waste, redundant abstractions, circular deps |
| 7 | `build` | build time, cache config, CI pipeline efficiency |
| 8 | `cost` | compute, storage, idle resources, token spend (if AI is present) |

4. A clearly N/A lane (no UI → skip re-render checks) → mark `skipped` with a reason; never skip silently

### 2. Dispatch Subagents

> Goal: review every dimension at once

1. Use `/use-subagents` to spawn one optimize review subagent per relevant lane — ≤10 per batch per `/follow-parallel`
2. Each subagent receives: `workspace-path`, `lane`, `file-ownership` — output contract: findings table (`No.`, `Finding`, `Impact`, `Effort`, `Evidence`, `Fix`) + lane score
3. A subagent reads only the files in its ownership — never sweep the whole codebase, never edit code (report-only)
4. A lane with ≤ 2 findings → the parent analyzes it itself
5. A failed subagent → mark `failed` and write that lane in the report as `review-failed` — never silently

### 3. Aggregate And Prioritize

> Goal: one plan ordered by impact

1. Merge findings from every lane — dedup by `file + root-cause`
2. Set priority by `impact × blast-radius`: high-impact P0 quick-wins always come first
3. Order execution: Foundation → Dependencies → High impact → Critical path → High risk
4. For every item, state the expected gain (e.g. bundle -X kb, query -Y ms) where estimable + a rough effort

### 4. Report (And Optional Apply)

> Goal: a plan ready to execute once confirmed

1. Run `/report` — `## Optimization Plan`: table of `No.`, `Lane`, `Finding`, `Impact`, `Effort`, `Priority`, `Evidence`, `Owner`
2. persist → `.devin/temp/report/<workspace>/deep-optimize-<time>.md` per `/create-report-in-dot-devin` (if present)
3. `--apply` + user confirm → apply fixes in plan order via `/implement-to-production` one item at a time, verifying every round
4. Run `/suggest-next-action`

## Rules

- report-only by default — fix only with `--apply` and user confirm
- every finding must have evidence (file:line, metric, or measurement) — never guess a bottleneck from intuition
- measure before proposing complex optimizations — a micro-optimization without evidence → don't propose it
- don't propose a large architecture change without a clear expected gain
- preserved behavior: an optimization must not change output/public API (except deliberate performance fixes)
- Use /deep-optimize when needed (deep-dive a single lane)
- Use /deep-analyze when needed (root cause unclear)
- Use /deep-review-codebase when needed (all review-*, not just optimization)
- Use /deep-test load to gather perf evidence for throughput/latency lanes

## Expected Outcome

- An optimization plan covering every dimension with evidence and priority
- Quick wins separated from strategic optimizations
- skipped/failed lanes reported with a reason — coverage is verifiable
