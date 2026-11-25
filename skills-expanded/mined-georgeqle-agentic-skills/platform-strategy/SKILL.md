---
name: platform-strategy
description: Expand from a single product into a multi-product platform — map vertical and horizontal growth vectors, score candidates, design validation experiments, and sequence the portfolio
type: research
version: v0.9
argument-hint: "[optional: expansion direction e.g. \"vertical\", \"horizontal\", or specific adjacent market]"
interview_depth: light
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Platform Strategy — Multi-Product Expansion Planning

Invoke as `$platform-strategy`.

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

## Prerequisites

**Required (at least one):**
- `research/icp.md` (or `research/{slug}/icp.md`) — who you serve today
- A working product/codebase to analyse for extensibility

If neither exists, tell the user: "Platform expansion requires a foundation. Run `$customer-discovery` first to define who you serve today, then come back."

**Strongly recommended** (read if they exist):
- `research/competitive-analysis.md` — market gaps
- `research/journey-map.md` — user flows, drop-off points
- `research/metrics.md` — retention, activation baselines

**Optional:** `research/monetization.md`, `research/positioning.md`, `research/customer-feedback.md`, `research/enterprise-icp.md`, `research/assumption-tracker.md`

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

### 1. Assess Core Product Health

Read the codebase, existing research, and metrics to evaluate: PMF signals (retention, activation, satisfaction), technical extensibility (shared infra — auth, billing, data — vs. tightly coupled), team/resource signals, revenue stability.

**Checkpoint 1 — Present core health assessment.** Show health summary, shareable infrastructure, red flags. Ask: "Does this match your sense of where the core product is? Resource constraints to factor in?"

### 2. Map Expansion Vectors

Use web search with **8-12 diverse queries**: adjacent markets, vertical depth (enterprise features, advanced use cases), horizontal breadth (related categories, tools used alongside), platform precedents, user workflow gaps, ecosystem opportunities, acquisition patterns, market trends, adjacent pain points, bundling precedents.

Also analyse codebase and existing research for internal signals: adjacent feature requests from customer feedback, competitor product lines, journey map drop-offs, data/infra that could power new products.

### 3. Identify Expansion Candidates — Present & Validate

Cluster findings into **4-8 candidates** across two axes:

**Vertical:** advanced tiers, deeper workflow coverage, industry-specific variants, data products from existing data.

**Horizontal:** complementary tools, adjacent persona products, same tech applied to different problem, marketplace/platform plays.

For each: problem, audience, relationship to core, market signal, vertical vs. horizontal.

Record the 4-8 candidates in `research/.progress.yaml` as `product_paths[]` entries with `source_skill: platform-strategy`. The top candidate may be `status: active` or `status: revisit_candidate` depending on whether the user is ready to validate it now; non-selected candidates should default to `status: deferred` with validation triggers. Include `id`, `label`, `source_skill: platform-strategy`, `pipeline_stage: platform-strategy`, `scope_path`, `status`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, and `last_touched`.

**Checkpoint 2 — Present candidates.** Group by vertical/horizontal with rationale and evidence. Ask: "Expansion directions I missed? Any clearly wrong? Internal signals pointing toward any of these?"

### 4. Score Expansion Candidates

Score each across five dimensions (1-5 each):

- **Synergy** — shared users, data, infra, cross-sell potential
- **Market Opportunity** — size, competitive density, willingness to pay, growth
- **Effort & Risk** — build complexity, time to revenue, tech risk, cannibalization
- **Strategic Value** — defensibility, brand coherence, sequencing value
- **Validation Cost** — how cheaply can we test demand

Build a scoring matrix with weighted totals.

### 5. Design Validation Experiments for Top Candidates

For **top 2-3 candidates**: cheapest test method (landing page, fake-door, survey, pre-sale, concierge), audience, success criteria, timeline (1-4 weeks), decision rules (proceed/pivot/kill). Reference `$experiment` for full experiment design.

### 6. Sequence the Portfolio — Present & Validate

Recommend a portfolio sequence: **Now** (next quarter), **Next** (quarter +1), **Later** (6-12 months), **Watch** (12+ months). For each: shared infra needed, dependencies, revenue expectation, kill criteria.

**Checkpoint 3 — Present full portfolio plan.** Show scoring matrix, validation experiments, portfolio sequence, shared platform considerations. Ask: "Sequencing match your priorities? Different experiments to run first? Dependencies I'm missing?"

### 7. Write Output

Only after user validates, write the output files.

## Deliverables

- `research/platform-strategy.md` (or `research/{slug}/platform-strategy.md`) — Full platform strategy: summary, core health, expansion vector map, scoring matrix, validation experiments, portfolio sequence, shared platform considerations, next steps.
- `research/platform-strategy-search-log.md` (or `research/{slug}/platform-strategy-search-log.md`) — Raw research log: every query, findings, source attribution, scoring rationale.
- `research/.progress.yaml` — product-path manifest updated with 4-8 expansion candidates. This does not require every candidate to become a full research track.

`## Next Steps` section with a **Recommended** item and **Other options** (2–4 alternatives). Use this format in the output:

## Next Steps

**Recommended:** `$experiment [top candidate]` — validate demand for the highest-scored expansion candidate before committing resources

Other options:
- `$assumption-tracker` — track which platform assumptions need validation (if no `research/assumption-tracker.md`)
- `$competitive-analysis [adjacent category]` — research the competitive landscape for the top expansion candidate
- `$customer-discovery [new audience]` — run customer discovery for the new audience the top candidate targets
- `$enterprise-icp` — map enterprise requirements if the expansion targets enterprise (if no `research/enterprise-icp.md`)
- `$roadmap` — sequence the expansion into the build plan (if `specs/` exist for the candidate)
- `$roadmap` — sequence the expansion into the build plan (if `specs/` exist)

The recommendation (`$experiment [top candidate]`) is always applicable — platform expansion should be validated before built.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Use web search extensively — every market signal must trace to research evidence.
- Cite sources for market signals, competitor product lines, trend data.
- Be honest about uncertainty.
- Stay in strategy mode — no architecture, features, or technical solutions.
- Core health is gating — flag PMF problems directly.
- Score honestly — low-synergy, high-effort candidates should score low.
- Present before writing — never write until findings are validated.
- Do not overwrite existing `research/platform-strategy.md` (or `research/{slug}/platform-strategy.md`) without asking.
- Keep validation experiments lightweight — full design belongs in `$experiment`.
- `## Next Steps` must be the final section in the output file, with a recommended next step and 2–4 other options.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/platform-strategy-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
