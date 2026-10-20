---
name: repo-audit-reporting
description: Create concrete repository audit reports with provenance, live seam tracing, ranked findings, and exact code references. Use when the user asks for a report, audit, writeup, inventory, blast-zone analysis, choke-point analysis, production-blocker review, code-reduction plan, or "how does this work" document about duplicate plus drift code, local-vs-package overlap, import/env/session contract drift, terminology overload, Athena/query ownership, or subsystem operation maps such as upload/storage/table-sync flows.
---

# Repo Audit Reporting

## Overview

Create repo-native audit reports that explain what is live now, what duplicates or drifts, how a subsystem actually works end to end, and what should be reduced first. Prefer evidence-rich writeups over generic summaries.

## Choose the report family

- For duplicate-plus-drift, local-vs-package forks, or blast-zone reduction reports, read [references/drift-and-overlap.md](references/drift-and-overlap.md).
- For "what is slowing development most", "what blocks production", "what should we delete first", or "where is the ambiguity/choke point" reports, read [references/choke-points-and-reduction.md](references/choke-points-and-reduction.md).
- For subsystem operation maps, upload/storage flows, or "how does this table stay updated" reports, read [references/operation-and-sync.md](references/operation-and-sync.md).
- For deep import, env fallback, auth base URL, or server-session provenance drift, read [references/env-session-import.md](references/env-session-import.md).
- If the request spans multiple families, read each relevant reference and merge them into one report with clearly separated sections.

## Workflow

1. Anchor on the live seam first.
   - Trace the page, hook, store, route, service, and repository chain before classifying anything as stale or duplicated.
   - Prefer import tracing and route tracing over broad text counts.

2. Establish a provenance baseline.
   - Capture `git rev-parse --short HEAD`.
   - Capture the latest commit subject.
   - Check whether the worktree state matters for the report.

3. Gather evidence with focused search.
   - Use `rg` for imports, route paths, helper names, duplicate state shells, mutation calls, refresh/refetch paths, env fallback chains, and session resolution seams.
   - Read the concrete files that define the behavior; do not rely on file names alone.

4. Separate statuses explicitly.
   - Distinguish `active runtime seam`, `adapter seam`, `duplicate plus drift`, `legacy but still present`, and `dead candidate`.
   - Do not label code dead until consumers are checked.

5. Measure only when it adds value.
   - For cleanup reports, include file counts, line counts, or cluster inventories when ranking by reduction leverage.
   - For operational reports, prioritize flow clarity over counts.
   - For choke-point reports, measure only the seams that materially explain development drag, ownership ambiguity, or production risk.

6. Write the report as a working artifact.
   - If the repo already uses `docs/audits/`, write the report there.
   - Use filenames that include the date and topic.
   - Link to exact local files in the report.

7. State the real source of truth.
   - Say whether the behavior is database-backed, storage-backed, cache-backed, or purely client state.
   - Call out legacy routes, stale wrappers, and cosmetic-only UI shells separately from the live path.

## Output requirements

- Start with a title, date, and one-paragraph scope statement.
- Add a provenance section with the commit baseline and how the audit was built.
- Prefer these section sets:
  - Drift or overlap: `Executive Summary`, `How This Audit Was Built`, `Cluster Inventory`, `Highest Value Remaining Refactors`, `Cluster Notes`
  - Choke point or reduction: `Executive Summary`, `How This Audit Was Built`, `Cluster Inventory`, `Highest Value Remaining Refactors`, `Production Blockers`, `Recommended Reduction Sequence`, `Cluster Notes`
  - Operation or sync: `Executive Summary`, `Entry Point`, `UI Surface Map`, `Live Operation Map`, `How State Stays Updated`, `Gaps And Caveats`
  - Env or session: `Methodology`, `Headline Numbers`, `Ranked Findings`, `Recommended Seam`
- Rank findings by runtime risk or refactor value, not only raw line count.
- When the same word names multiple live seams, call that terminology overload out explicitly and separate the clusters by meaning.
- Say explicitly when a bulk-action bar, refresh button, or helper abstraction exists but is not fully wired.

## Reference routing

- Read [references/drift-and-overlap.md](references/drift-and-overlap.md) for duplicate, fork, and package-replacement audits.
- Read [references/choke-points-and-reduction.md](references/choke-points-and-reduction.md) for development-drag, blocker, reduction-order, and code-deletion-first audits.
- Read [references/operation-and-sync.md](references/operation-and-sync.md) for subsystem flow and synchronization reports.
- Read [references/env-session-import.md](references/env-session-import.md) for import, env, and session provenance audits.
