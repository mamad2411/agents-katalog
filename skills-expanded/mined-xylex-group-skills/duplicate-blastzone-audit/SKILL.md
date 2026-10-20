---
name: duplicate-blastzone-audit
description: Find similar or duplicate functions across a codebase, map blast zones of callers and dependents, rank clusters by yield (highest refactor payoff) and risk (runtime/coupling danger), and produce actionable reports with where to start. Use when the user asks for duplicate functions, similar logic, blast zone analysis, dedup opportunities, drift between copies, highest-yield cleanup, reduction order, or "what should we consolidate first". Triggers on duplicate function audit, blast zone report, yield ranking, risk ranking, similar helpers, parallel implementations. Use when the user runs /duplicate-blastzone-audit.
---

# Duplicate Blastzone Audit

## Goal

Turn "find duplicate or similar functions" into a ranked, risk-aware reduction plan. Discover function-level clusters, measure each cluster's **blast zone** (who calls it, what breaks if you merge), score **yield** (payoff per effort), score **risk** (what could go wrong), and name the **best first slice**.

## Quick Start

1. Anchor on the live seam the user cares about (route, command, handler, export).
2. Discover duplicate/similar **functions** (not just files) via symbol search, signature patterns, and behavior tracing.
3. Build function clusters with evidence: names, paths, line spans, drift notes.
4. Map blast zones: direct callers, transitive importers, tests, generated code, docs.
5. Score yield and risk per cluster using [references/yield-risk-rubric.md](references/yield-risk-rubric.md).
6. Write the report from [references/report-template.md](references/report-template.md).
7. End with **Start here** — one cluster, one canonical target, one safe first PR.

## Modes

| Mode | When | Deliverable |
|------|------|-------------|
| **Discover** | "find duplicates", broad audit | Function cluster inventory + blast zones |
| **Rank** | inventory exists or user names seams | Yield/risk matrix + ordered backlog |
| **Plan** | "where to start", "reduction order" | Start-here slice + phased sequence |
| **Reduce** | user wants implementation | Consolidate one cluster + drift guardrail |

Default to **Discover + Rank** unless the user only wants a plan from known clusters.

## Function Discovery Workflow

### 1. Establish the live seam

- Trace production entrypoints before auditing.
- Do not label functions dead until caller tracing agrees.
- Prefer import/symbol tracing over raw text similarity.

```powershell
rg -n "fn\s+\w+|function\s+\w+|const\s+\w+\s*=\s*\(|export\s+(async\s+)?function" src/ crates/
rg -n "pub\s+fn\s+\w+" --type rust
rg -n "export\s+(async\s+)?function|export\s+const\s+\w+" --type ts
```

### 2. Find duplicate and similar functions

Use multiple signals; require at least two before clustering:

| Signal | How |
|--------|-----|
| **Same name** | `rg -n "fn resolve_session|function resolveSession"` across paths |
| **Same signature shape** | Similar params/return types, serde fields, error variants |
| **Same behavior** | Shared call sequence (validate → fetch → map → return) |
| **Copy-paste drift** | Near-identical bodies with small conditional differences |
| **Parallel wrappers** | Thin adapters around the same underlying operation |

Cluster types:

- `Exact duplicate` — same behavior, merge is mechanical
- `Similar` — same intent, different policy or edge cases
- `Duplicate + drift` — copies already behave differently (**highest priority**)
- `Dead candidate` — no live callers after blast zone trace

### 3. Map the blast zone

For each function in a cluster, trace:

1. **Direct callers** — functions/modules that invoke it
2. **Transitive surface** — routes, CLI commands, jobs, public exports that reach it
3. **Tests** — unit/integration tests asserting behavior
4. **Generated dependents** — OpenAPI, SDK, MCP catalog, protobuf
5. **Docs/examples** — README, inline docs referencing the old path

```powershell
rg -n "symbol_name\(" .
rg -n "use\s+.*::symbol_name|from\s+.*import\s+.*symbol_name" .
rg -l "symbol_name" tests/ spec/ __tests__/
```

Draft a manifest using [references/function-cluster-manifest.example.json](references/function-cluster-manifest.example.json), then run:

```powershell
python scripts/blastzone_metrics.py --manifest path\to\clusters.json --repo .
```

Use output for: caller file count, symbol references, cluster line footprint, missing paths.

Read [references/blastzone-matrix.md](references/blastzone-matrix.md) for blast zone tiers and choke-point rules.

### 4. Score yield and risk

Apply [references/yield-risk-rubric.md](references/yield-risk-rubric.md) to every cluster.

- **Yield** = payoff if consolidated (lines saved × surface breadth × extraction readiness × drift pressure)
- **Risk** = danger of merging now (runtime criticality × blast radius × test gap × coupling)

Plot mentally on a 2×2:

```
high yield │ DO FIRST      │ STAGE CAREFULLY
           │ (quick wins)  │ (high value, high risk)
───────────┼───────────────┼──────────────────
low yield  │ BUNDLE LATER  │ DEFER / SKIP
           │               │
           low risk        high risk
```

**Start here** = top-left quadrant, or highest yield where risk is acceptable with a thin first PR.

### 5. Choose canonical authority

Per cluster, pick one:

- **Keep A** — merge B→A when A is on the live seam and better tested
- **Extract C** — new shared helper when both copies are wrong authority
- **Translate** — keep both only with explicit mapper when semantics differ by design

Record: canonical symbol, canonical path, dependents to repoint, tests to move.

### 6. Write the report

Use [references/report-template.md](references/report-template.md). Required sections:

- Executive summary with **Start here**
- Provenance (`git rev-parse --short HEAD`)
- Function cluster inventory (not just file inventory)
- Blast zone summary per cluster
- Yield/risk ranked table
- Recommended reduction sequence (phased)
- Per-cluster notes with exact paths and symbols

If the repo uses `docs/audits/`, write there with `YYYY-MM-DD-<topic>-blastzone-audit.md`.

## Fix / Reduce Mode

When implementing consolidation:

1. One function cluster per PR when possible
2. Repoint callers to canonical symbol first; delete duplicate last
3. Add or move tests to canonical path before deleting copies
4. If copies drifted, add a regression test locking intended behavior
5. Regenerate downstream artifacts if blast zone includes generated surfaces

For file-level dead-code quantification and blame snapshots, also load `$audit-duplicate-dead-code`.

For formal drift/overlap writeups with package-fork analysis, also load `$repo-audit-reporting`.

For Rust contract authority after dedup, also load `$rust-contract-spine`.

## Output Checklist

- [ ] Every cluster lists **functions/symbols**, not only directories
- [ ] Blast zone counts (callers, routes, tests) per cluster
- [ ] Yield and risk scores with one-line justification each
- [ ] **Start here** names one cluster + canonical target + first PR scope
- [ ] `Duplicate + drift` outranks plain duplication in rank order
- [ ] Dead claims backed by caller trace, not grep alone
- [ ] Reduction sequence respects risk (low-risk extractions before auth/payment seams)

## Reference Map

- [references/blastzone-matrix.md](references/blastzone-matrix.md) — blast zone tiers, choke points
- [references/yield-risk-rubric.md](references/yield-risk-rubric.md) — dual-axis scoring
- [references/report-template.md](references/report-template.md) — report skeleton
- [references/function-cluster-manifest.example.json](references/function-cluster-manifest.example.json) — machine-readable cluster input