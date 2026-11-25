---
name: cli-audit-xray
metadata:
  author: clement
description: >
  Reveal hidden semantic, mathematical, dataflow, resource-flow, and operational structure in code.
  Produces optimization candidates with explicit invariants, risks, validation methods, and handoffs.
  Use when analyzing a function, hot path, AI inference pipeline, compiler/runtime bottleneck,
  DevSecOps pipeline, LLM gateway, distributed system, or complex business logic for missed
  optimization opportunities. Also triggers on "semantic xray", "semantic optimization graph",
  "hidden structure", "optimization cards", "dataflow optimization", "resource flow",
  "repeated computation", "unnecessary allocation", "cache placement", "CPU/GPU boundary",
  "prove this optimization", "is this rewrite safe", or "find optimizations humans miss".
argument-hint: "[file-or-directory-or-hot-path]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are written in English. When generating user-facing output (reports, files, documentation), detect the project's primary language (from README, comments, docs, commit messages) and produce the output in that language. If the project is bilingual, ask the user which language to use before proceeding.

# Audit X-Ray — Semantic Optimization Scanner

Reveal what the code is really doing before proposing optimizations. The output is not "make it faster"; it is a ranked set of falsifiable optimization candidates with locations, invariants, validation methods, and handoffs to the skills that can prove or implement the next step.

Core rule:

> First reveal structure. Then propose hypotheses. Then classify risk. Then validate.

## What This Skill Adds

`cli-audit-xray` sits between static code quality, topology, drift, and performance work:

- `cli-audit-code` finds quality smells; X-Ray finds hidden semantic cost in otherwise acceptable code.
- `cli-audit-tangle` finds graph shape; X-Ray adds dataflow, resource flow, and optimization meaning to hot or tangled paths.
- `cli-audit-drift` checks code against contracts; X-Ray extracts missing invariants that should become contracts.
- `cli-forge-perf` proves runtime gains; X-Ray produces candidates worth benchmarking.

## Input

`$ARGUMENTS` is the target to inspect:

- **Function or file**: build a focused Semantic Optimization Graph around that code.
- **Directory**: sample likely hot paths, entrypoints, adapters, pipelines, and large loops.
- **Trace/flamegraph/profile path**: use the dynamic evidence to focus static inspection.
- **Empty**: inspect `src/` or the primary source directory at a shallow level.

## Mitosis — Scale Analysis to Scope

Reference `../shared/tiering.md` for canonical S/M/L/XL semantics.

| Scope | Tier | Behavior |
|---|---|---|
| One function / one hot path | **S** | Full semantic map + up to 5 optimization cards |
| One file / small module | **M** | Dataflow + resource flow + ranked cards |
| Directory / service slice | **L** | Sample top 10-15 risky paths; use tangle/perf evidence if available |
| Monorepo / distributed system | **XL** | Do not deep-scan everything; produce map of candidate zones and handoffs |

Bias down when unsure. A noisy X-Ray report is worse than a narrow one with strong evidence.

## Workflow

### Step 0 — Load Shared Contracts

Before producing findings:

1. Read `../gotchas.md` if it exists.
2. Read `../shared/optimization-card.md` for the canonical card contract.
3. Read `../shared/triage.md` for tier/confidence semantics.
4. Read `../shared/done-gate.md` and `../shared/gate-ladder.md` when a candidate requires proof or benchmark.
5. If present, read `.claude/tangle-partition.json` to focus on god functions, cycles, and boundary functions.
6. If present, read `CONTRACTS.md` before proposing rewrites that depend on behavior or invariants.

### Step 1 — Build the Mental SOG

Use `references/semantic-optimization-graph.md` for node types and mapping rules.

Extract:

- operations and transformations;
- data objects and shapes;
- control flow, loops, retries, async waits;
- resource flow: allocations, copies, serialization, locks, I/O, network, CPU/GPU boundaries;
- constraints and invariants;
- observable side effects;
- security and trust boundaries.

### Step 2 — Lift Where Useful

Use `references/optimization-families.md` when looking for patterns.

Lift imperative regions into maps, filters, reductions, scans, joins, state machines, tensor operations, graph traversals, policy decisions, or equations. Do not force math when it adds no decision value.

### Step 3 — Discover Candidates

Look for:

- repeated computation;
- common subexpressions;
- loop-invariant work;
- map/filter/reduce fusion;
- needless materialization;
- clone/copy/allocation hot spots;
- serialization/deserialization churn;
- bad cache placement;
- network or database calls inside loops;
- lock scope around I/O;
- CPU/GPU or device/host roundtrips;
- misplaced validation, DLP, auth, or policy boundaries.

### Step 4 — Gate Every Candidate

For each candidate, answer:

- What must be true?
- What could break?
- Which invariant is missing?
- How can we validate it?
- Is this a proof problem, benchmark problem, test problem, or architecture problem?

Use `references/risk-rules.md` for floating point, side effects, concurrency, and security boundaries.

### Step 5 — Report and Emit Envelope

Produce a Markdown report and, when running under `cli-cycle` or when writing files is allowed, emit `.claude/cli-audit-xray.json` following `../shared/result-schema.md`.

## Output Format

```markdown
# Semantic X-Ray Audit — {project-or-scope}

**Target**: {file/directory/hot path} | **Language**: {detected} | **Date**: {date}
**Scope tier**: S/M/L/XL | **Candidate count**: N

## Executive Summary
- Hidden structure found:
- Highest-leverage candidate:
- Highest-risk assumption:
- Next proof step:

## Semantic Map
### Dataflow
### Control Flow
### Resource Flow
### Trust / Security Boundaries

## Hidden Invariants
| Invariant | Evidence | Missing? | Downstream use |

## Optimization Candidates
{optimization cards using ../shared/optimization-card.md}

## Handoffs
| Target skill | Scope | Reason |

## Validation Plan
Map candidates to unit tests, property tests, benchmarks, trace comparisons, or contracts.
```

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|---|---|---|
| Candidate requires runtime measurement, profile, or A/B proof | `/cli-forge-perf` | Use native benchmark protocol and significance gate |
| Candidate depends on an implicit behavior invariant | `/cli-audit-drift` | Promote the invariant into CONTRACTS.md or verify existing contract |
| Candidate sits in a god function, cycle, or unclear boundary | `/cli-audit-tangle` | Restructure or isolate before optimizing |
| Candidate needs new property/unit/negative tests | `/cli-audit-test` | Validate equivalence and prevent regressions |
| Semantic graph is useful to humans (> 12 nodes or cross-boundary flow) | `/cli-forge-schema` | Render Mermaid from the semantic map |
| Candidate touches auth, DLP, audit logs, retry, backpressure, or failover | `/cli-forge-resilience` | Treat it as operational risk, not only optimization |
| Candidate needs a CI perf gate or reproducible baseline | `/cli-forge-pipeline` | Make the validation repeatable in CI |

**Rule:** Recommend, don't auto-execute. Phrase as: "Consider running `/cli-forge-perf` — candidate X needs a reproducible A/B benchmark."

When running under `cli-cycle`, audit targets that usually run earlier (`cli-audit-tangle`, `cli-audit-drift`, `cli-audit-test`) are report-only recommendations if they already ran. Do not emit backward automatic handoffs that create a cycle; use their existing outputs when available.

## Rules

1. **No optimization claim without preconditions.** Say "valid if..." instead of "correct."
2. **No runtime gain claim without measurement.** If hardware, compiler, backend, cache, shape, distribution, or workload matters, mark it benchmarkable.
3. **Security before speed.** Do not move, remove, cache, or deduplicate auth/DLP/policy/audit behavior unless the trust boundary is preserved.
4. **Floating-point is not algebra over reals.** Mention NaN, infinity, rounding, overflow, underflow, tolerance, and order effects.
5. **Side effects are semantics.** Logging, metrics, mutation, global state, time, randomness, I/O, exceptions, cancellation, and locks can invalidate rewrites.
6. **Concrete locations only.** Every card should have `file:line` evidence when source is available.
7. **Do not fix by default.** This skill reports candidates and patch plans. Use explicit user direction before editing code.

## Integration with other cli-* skills

| Skill | Relationship |
|---|---|
| `cli-forge-perf` | X-Ray proposes benchmarkable candidates; perf proves or rejects them |
| `cli-audit-code` | Code quality can flag local smells that X-Ray turns into semantic-cost candidates |
| `cli-audit-tangle` | Tangle supplies topology and boundary functions; X-Ray supplies data/resource meaning |
| `cli-audit-drift` | Drift supplies contracts; X-Ray supplies missing invariants and rewrite preconditions |
| `cli-audit-test` | X-Ray identifies equivalence/property tests required by optimizations |
| `cli-forge-schema` | Renders semantic maps and resource-flow diagrams |
| `cli-forge-pipeline` | Turns recurring validation into CI gates |
| `cli-cycle` | Can run X-Ray as an adaptive Wave 2/3 audit and aggregate its JSON envelope |

## What This Skill Does NOT Do

- **Does not replace profilers.** It finds hypotheses; perf proves dynamic cost.
- **Does not replace topology analysis.** Use `cli-audit-tangle` for call graph partitioning.
- **Does not replace contracts.** Use `cli-audit-drift` to check intention vs implementation.
- **Does not auto-rewrite.** It can propose patch plans, but changes require explicit user direction.
