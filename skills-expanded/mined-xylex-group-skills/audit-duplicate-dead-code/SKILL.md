---
name: audit-duplicate-dead-code
description: Audit repositories for duplicate code, dead code, refactor hotspots, and drifted parallel implementations. Use when Codex needs to cluster repeated logic, prove a legacy tree is dead, quantify file counts and line savings, capture git blame ownership, or produce a ranked markdown cleanup report with tracker-ready follow-ups.
---

# Audit Duplicate Dead Code

## Overview

Turn a loose "find duplicate or dead code" request into a durable audit artifact. Confirm the live runtime seam first, cluster related files by behavior, quantify footprint and ownership, then write a ranked markdown report that is useful for cleanup planning or tracker backfill.

## Workflow

1. Establish the seam before auditing.
2. Build behavior-level clusters instead of isolated text matches.
3. Prove whether each cluster is duplicate, dead, or duplicate plus drift.
4. Quantify each cluster with current file counts, total lines, and blame ownership.
5. Rank by refactor value, not only by deletable lines.
6. Write a report that a maintainer can act on without rerunning the whole audit.

## 1. Establish The Seam

- Start from the live route, import, handler, or entrypoint that the user actually cares about.
- Confirm what code is active now before calling anything dead.
- Prefer `rg` and import tracing over assumptions.
- When a legacy tree looks dead, follow the current runtime seam end to end first.

Examples:
- Public routes moved to a new App Router seam while an old module tree still exists.
- Two route tests carry the same Athena/session/mock harness.
- Builder shells or modal sections repeat the same state lifecycle.

## 2. Build Clusters

- Group by behavior seam, not by a single repeated utility call.
- Prefer clusters like "single-step vs multi-step public form flow" over vague clusters like "two files both call `toast`".
- Include every file that materially participates in the repeated seam.
- If a cluster is partially consolidated already, include the new shared helper so the report shows the whole surface.

Good cluster types:
- Duplicate
- Dead candidate
- Duplicate plus drift

## 3. Prove The Classification

- Mark a cluster as `Dead candidate` only after grep, import tracing, and runtime seams agree it is no longer used.
- Mark a cluster as `Duplicate + drift` when the copies no longer behave the same way.
- Treat `Duplicate + drift` as higher priority than plain duplication.
- Call out partial cleanup separately from not-started cleanup.

Use these commands routinely:

```powershell
rg -n "pattern" .
rg --files | rg "path-fragment"
git log --stat -- <path>
git blame --line-porcelain -- <path>
```

## 4. Quantify The Cluster

- Draft a manifest using [references/cluster-manifest.example.json](references/cluster-manifest.example.json).
- Run:

```powershell
python scripts/cluster_metrics.py --manifest path\to\clusters.json
```

- Use the script output for:
  - file count
  - total lines
  - blame snapshot
  - missing files that need manual review
- Recheck outliers manually before publishing the report.
- Keep `total lines` separate from `estimated savings`.

## 5. Rank By Refactor Value

- Read [references/ranking-rubric.md](references/ranking-rubric.md) before ordering the final list.
- Let live runtime drift outrank simple line-count cleanup.
- Prefer broad maintenance wins over tiny one-off deletions.
- Treat large, low-risk dead-code removal as high value, but still below live user-facing correctness seams.
- Bundle tiny clusters into adjacent work instead of inflating them into standalone projects.

## 6. Write The Report

- Start from [references/report-template.md](references/report-template.md).
- Include:
  - methodology
  - provenance
  - cluster inventory
  - highest-value remaining refactors
  - already-landed consolidations
  - cluster notes
  - tracker backfill, if applicable
- Attribute with a `git blame` snapshot instead of guessing ownership.
- If a worktree is already clean, write the report as a repo-head audit artifact instead of pretending there is an active diff.

## Output Checklist

- Confirm the live seam for every dead-code claim.
- Show current file count and total lines for every cluster.
- Show estimated savings separately from footprint.
- Include blame ownership for every cluster.
- Rank by value, not only by size.
- Keep reason notes short and specific.
- Link the concrete files or directories behind each cluster.
