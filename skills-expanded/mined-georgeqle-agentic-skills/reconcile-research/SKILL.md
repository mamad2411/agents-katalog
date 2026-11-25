---
name: reconcile-research
description: Cross-document consistency audit across research outputs — find contradictions, stale assumptions, and gaps
type: research
version: v0.9
argument-hint: "[audit|fix] [all|icp|pricing|journey|enterprise|feedback|specs]"
interview_depth: none
---

# Reconcile Research — Cross-Document Consistency Audit

Invoke as `$reconcile-research`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page with the full preliminary packet, evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 1. Determine Mode and Scope

Parse `$ARGUMENTS`:

- **Mode**: `audit` (default, read-only) or `fix` (apply approved changes, write reconciliation report)
- **Scope**: `all` (default), `icp`, `pricing`, `journey`, `enterprise`, `feedback`, or `specs`

### 2. Inventory Research Documents

Scan `research/` for main documents. Skip files matching `*-search-log.md` and `*-interview.md` — these are raw logs, not assertion-bearing documents.

**Expected documents** (not all need to exist):
- `research/icp.md` (cross-path overview), `research/{slug}/icp.md` (per-product-path)
- `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`)
- `research/journey-map.md` (or `research/{slug}/journey-map.md`)
- `research/metrics.md` (or `research/{slug}/metrics.md`)
- `research/gtm.md` (or `research/{slug}/gtm.md`)
- `research/monetization.md` (or `research/{slug}/monetization.md`)
- `research/enterprise-icp.md` (or `research/{slug}/enterprise-icp.md`)
- `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`)

When `research/` contains subdirectories, scan each `research/{slug}/` for per-product-path documents.

**Stop condition**: If fewer than 2 research documents exist, display a message and exit — there's nothing to reconcile.

### 3. Extract Claims

Launch a **subagent per document** to extract structured claims. Each subagent reads one file and returns claims in these categories:

| Category | Examples |
|----------|----------|
| **ICP targets** | Primary persona, company size, industry, geography |
| **Pain points** | Problems the product solves, severity rankings |
| **Budget signals** | Willingness to pay, price sensitivity, deal size |
| **Channels** | Acquisition channels, distribution strategy |
| **Messaging** | Value propositions, positioning statements |
| **Pricing** | Model type, price points, tier structure, usage limits |
| **Journey stages** | Stage names, transitions, aha moments, activation criteria |
| **Metrics** | North star, per-stage metrics, thresholds |
| **Competitors** | Named competitors, positioning relative to them |
| **Deal-killers** | Enterprise blockers, compliance requirements |
| **Feedback verdicts** | Validated assumptions, invalidated assumptions, new findings |

Each claim includes the source file, section heading, and a direct quote for traceability.

### 4. Cross-Reference Checks

Launch **subagents per scope group** to run pairwise checks. Only run checks where both documents in a pair exist.

#### `icp` scope — ICP vs all downstream (11 checks)

Requires: `research/icp.md` + at least one downstream document.

| # | Check | Documents | What to flag |
|---|-------|-----------|--------------|
| 1 | User profile consistency | ICP ↔ Journey Map | Journey references personas not defined in ICP |
| 2 | Pain point coverage | ICP ↔ Competitive Analysis | Competitive analysis addresses pains not in ICP, or misses ICP pains |
| 3 | Pain point → feature mapping | ICP ↔ Journey Map | Journey stages that don't map to any ICP pain point |
| 4 | Budget signal → pricing alignment | ICP ↔ Monetization | Pricing exceeds ICP budget signals, or ignores stated willingness-to-pay |
| 5 | Channel consistency | ICP ↔ GTM | GTM targets channels the ICP doesn't use, or misses primary ICP channels |
| 6 | Messaging ↔ value prop alignment | ICP ↔ GTM | GTM messaging doesn't reflect ICP's top pain points or value props |
| 7 | Market landscape agreement | ICP ↔ Competitive Analysis | ICP market sizing contradicts competitive analysis market data |
| 8 | Feedback invalidation | ICP ↔ Customer Feedback | Feedback explicitly invalidates ICP assumptions still stated as fact |
| 9 | Metric coverage of ICP goals | ICP ↔ Metrics | ICP success criteria not tracked by any metric |
| 10 | ICP ↔ enterprise profile conflicts | ICP ↔ Enterprise ICP | Base ICP and enterprise ICP contradict on overlapping fields |
| 11 | Geography/segment consistency | ICP ↔ GTM | GTM targets geographies or segments not mentioned in ICP |

#### `pricing` scope — GTM vs Monetization coherence (7 checks)

Requires: `research/gtm.md` + `research/monetization.md`.

| # | Check | What to flag |
|---|-------|--------------|
| 1 | Revenue model agreement | GTM and Monetization describe different revenue models |
| 2 | Price point consistency | GTM pricing references don't match Monetization's price points |
| 3 | Tier structure alignment | GTM tier names/features don't match Monetization tier definitions |
| 4 | Upgrade trigger consistency | GTM conversion triggers contradict Monetization's upgrade triggers |
| 5 | Expansion metric alignment | GTM growth metrics don't match Monetization's expansion revenue drivers |
| 6 | Aha moment → pricing gate | Monetization gates features before the aha moment defined in Journey Map |
| 7 | Free tier scope | GTM's free tier description contradicts Monetization's free tier limits |

#### `journey` scope — Journey Map vs Metrics/GTM/Monetization (7 checks)

Requires: `research/journey-map.md` + at least one of Metrics/GTM/Monetization.

| # | Check | What to flag |
|---|-------|--------------|
| 1 | Stage name consistency | Metrics or GTM reference journey stages by different names |
| 2 | Metric coverage per stage | Journey stages with no corresponding metric in Metrics |
| 3 | Aha moment agreement | Journey Map, Metrics, and Monetization define different aha moments |
| 4 | Activation criteria consistency | Journey Map activation ≠ Metrics activation definition |
| 5 | Channel → stage mapping | GTM channels don't map to the discovery/awareness stages in Journey Map |
| 6 | Conversion trigger alignment | Journey Map conversion triggers ≠ GTM conversion triggers |
| 7 | Retention stage coverage | Journey Map has retention stages that Metrics doesn't track |

#### `enterprise` scope — Enterprise ICP vs base docs (6 checks)

Requires: `research/enterprise-icp.md` + at least one base document.

| # | Check | What to flag |
|---|-------|--------------|
| 1 | Profile field conflicts | Enterprise ICP contradicts base ICP on overlapping demographics |
| 2 | Deal-killer coverage | Enterprise deal-killers not addressed in Journey Map or Monetization |
| 3 | Stakeholder journey gaps | Enterprise stakeholders have no corresponding journey in Journey Map |
| 4 | Pricing tier fit | Monetization tiers don't include an enterprise tier matching Enterprise ICP needs |
| 5 | Lifecycle stage coverage | Enterprise evaluation→deployment→renewal lifecycle not reflected in Metrics |
| 6 | Compliance gap propagation | Enterprise compliance requirements not reflected in scale-audit or journey |

#### `feedback` scope — Customer Feedback propagation (5 checks)

Requires: `research/customer-feedback.md` + at least one other document.

| # | Check | What to flag |
|---|-------|--------------|
| 1 | Invalidated assumptions still present | Feedback marks an assumption as invalidated, but the source doc still states it as fact |
| 2 | New findings not captured | Feedback identifies new pain points or personas not reflected upstream |
| 3 | Severity mismatches | Feedback downgrades a pain point's severity, but ICP still lists it as primary |
| 4 | Staleness alerts | Documents haven't been updated since feedback was last appended |
| 5 | Contradicted positioning | Feedback contradicts GTM messaging or competitive positioning |

#### Product-path checks (3 checks)

Triggered when `research/` contains product-path subdirectories (e.g., `research/{slug}/icp.md`).

| # | Check | What to flag |
|---|-------|--------------|
| 1 | Cross-ICP consistency | Product-path ICPs (`research/{slug}/icp.md`) contradict each other on shared market assumptions |
| 2 | Shared pain point divergence | Same pain point described differently across product-path ICPs |
| 3 | Channel overlap conflicts | Product-path ICPs target the same channel with conflicting messaging |

### 5. Aggregate and Classify Findings

Collect all findings from the cross-reference subagents. Classify each by severity:

| Severity | Meaning | Example |
|----------|---------|---------|
| **Error** | Active contradiction — two documents assert incompatible facts | ICP says "SMB $50/mo budget" but Monetization's cheapest tier is $200/mo |
| **Warning** | Stale or gap — may be intentional but should be reviewed | Journey Map defines 5 stages but Metrics only covers 3 |
| **Info** | Suggestion — not wrong, but could be improved | GTM mentions a channel not discussed in ICP (may be a valid expansion) |

### 6. Walk Through Findings Interactively

Present findings **one at a time** using `request_user_input` (in Plan mode) or a plain-text question (otherwise), ordered by severity (Errors first, then Warnings, then Info). For each finding, present:

```
### [Scope] — [Check Name]
**Severity**: Error | Warning | Info
**Documents**: file-a.md ↔ file-b.md

**file-a.md** says:
> [direct quote from source]

**file-b.md** says:
> [direct quote from source]

**Contradiction**: [one-sentence description of the conflict]
**Recommended resolution**: [which document to update and why, based on dependency direction]

How would you like to resolve this? (Options: accept recommendation, update the other document instead, skip/defer, or provide custom instructions)
```

**Dependency direction** informs the recommended resolution:
- Upstream contradiction (e.g., ICP vs Journey Map) → recommend updating the downstream document
- Customer feedback contradictions → recommend updating upstream (feedback is ground truth)
- Peer contradictions (e.g., GTM vs Monetization) → note both are peers and ask which is authoritative

Wait for the user's response before proceeding to the next finding. Collect all decisions into a resolution list.

### 7. Apply Resolutions

After walking through all findings:

- **Audit mode** (default): Compile a summary of all findings and user decisions. Do not modify any files. Display the summary with the user's stated resolution for each item.
- **Fix mode** (if `fix` was specified):
  1. For each existing research document that will be replaced or substantively rewritten, archive the current file first, then apply the user-approved change to the canonical research document.
  2. Write `research/reconciliation-report.md` as an audit trail:

```markdown
# Reconciliation Report — [date]

## Resolved
- [Error/Warning description] — resolved by archiving and updating [file] per user decision: "[user's stated resolution]"

## Deferred
- [Description] — user chose to skip

## Info (no action)
- [Info items the user chose not to act on]
```

  3. Re-run the audit to confirm fixes resolved the flagged issues.

### 8. Populate Next Steps

After presenting findings (audit mode) or applying resolutions (fix mode), display a `## Next Steps` section with a **Recommended** item and **Other options**. Use this format:

## Next Steps

**Recommended:** [skill with most conflicts] — [N] conflicts traced to this document; re-running it will resolve the most inconsistencies at once

Other options:
- `$skill` — [N] conflicts in [scope] (re-run to fix)
- check `.agents/project.json.enabled_packs` for `research-admin` — if `research-admin` is not enabled, recommend `npx skillpacks install research-admin` from the project shell, first; if `research-admin` is enabled, recommend `$research-roadmap` — rebuild the ordered documentation queue after reconciliation
- check `.agents/project.json.enabled_packs` for `agent-work-admin` — if `agent-work-admin` is not enabled, recommend `npx skillpacks install agent-work-admin` from the project shell, first; if `agent-work-admin` is enabled, recommend `$spec-drift` — check whether code/spec drift remains after research reconciliation
- check `.agents/project.json.enabled_packs` for `agent-work-admin` — if `agent-work-admin` is not enabled, recommend `npx skillpacks install agent-work-admin` from the project shell, first; if `agent-work-admin` is enabled, recommend `$roadmap` — resequence implementation if reconciliation changed priorities

**Recommendation logic:** Identify the skill that produced the document with the most Error/Warning-severity conflicts. That skill is the recommendation — re-running it with current upstream context will resolve the most issues. List other conflict-bearing skills as alternatives, ordered by conflict count descending. If audit mode found only deferred items, or fix mode resolved every actionable conflict, check `.agents/project.json.enabled_packs` for `research-admin` — if `research-admin` is not enabled, recommend `npx skillpacks install research-admin` from the project shell, first; if `research-admin` is enabled, recommend `$research-roadmap` — check overall project status. If no conflicts, deferred items, or follow-up work remain, explicitly state "No follow-up skill recommended" instead of inventing work.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Read-only by default.** Only modify files when explicitly invoked with `fix` mode.
- **Never auto-resolve contradictions.** Errors always require user input on which side is correct. Use `request_user_input` (or plain-text question) for each finding individually.
- **Show evidence.** Every finding must include direct quotes from both documents.
- **Respect dependency direction.** Upstream documents are presumed authoritative over downstream, except customer feedback which is ground truth.
- **No false positives.** If uncertain whether something is a real contradiction, classify it as Info, not Error.
- **Skip absent documents.** Only run checks where both documents in a pair exist. Never flag a missing document as an error — that's `$research-roadmap`'s job.
- **Use subagents** for claim extraction (one per document) and cross-reference checks (one per scope group) to parallelize work.
- **Idempotent.** Running audit twice with no changes between should produce identical output.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/reconcile-research-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
