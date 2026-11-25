---
name: icp
description: Research-driven ICP discovery — web search + codebase analysis to identify multiple ICPs, pain points, value props, and cross-ICP prioritization
type: research
version: v0.9
argument-hint: <spec file path, concept/idea, or empty to use idea brief>
---

# ICP — Research-Driven Customer Discovery

Invoke as `$icp`.

## Report-First Approval Gate

Default to report-only: present findings, evidence coverage, assumptions, recommended artifact path, and proposed file changes in a pre-approval alignment page plus a concise conversation summary for user approval before creating or updating canonical research, spec, or task files.

Do not write or overwrite synthesized deliverables until the user explicitly approves, unless the user invoked an explicit write/update/fix mode or clearly asked to write files upfront. Raw evidence capture may be persisted before analysis when reproducibility requires it; report those raw paths separately and still gate synthesized research/report writes.

When stopping for approval, build and attempt to open the alignment preview page first, then ask the user to review it and approve, question, or request adjustments. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Research and clarify.** Perform the research, run required source/code checks, and ask any needed clarification questions. Write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Do not create or update canonical research, spec, or task files in Stage 1. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet.
2. **Stage 2 - Review alignment.** Consume the working packet and build the `review` HTML alignment page. The page must render the full preliminary packet, evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

Automated research that identifies **multiple ICP candidates**, maps pain points and value props, and selects a primary ICP. Uses web search + codebase analysis instead of interviews. If `research/idea-brief.md` or `research/{slug}/idea-brief.md` exists, use it as starting context for the research frame.

Default stance: assume the user has no insider knowledge of the market. Explain segments, pain signals, and tradeoffs from first principles so the recommendation is defensible without founder intuition. Ask for corrections, hard constraints, or proprietary facts only when needed.

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

1. **Parse input and gather concept context**:
   - Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Use `active_paths` to identify current product/app/ICP focuses and `product_paths[]` to preserve secondary product paths without treating them as git branches or parallel implementation lanes.
   - Read `$ARGUMENTS` as a spec file path or concept text when provided.
   - Read `research/{slug}/idea-brief.md` in product-path scope, or `research/idea-brief.md` in flat scope, when present. Treat it as starting context and source hypotheses, not as settled truth.
   - If `$ARGUMENTS` is empty and an idea brief exists, use the idea brief as the primary input before falling back to README, specs, or codebase inference.
   - If `$ARGUMENTS` conflicts with the idea brief, flag the mismatch at the first checkpoint and ask which premise should guide ICP research.
   - Read codebase if it exists. Read existing research for background.
   - **Use code/app hints secondarily** (`turbo.json`, `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `package.json` workspaces, app folders, or package folders) only after product-path resolution. If multiple active product paths exist, or if this run is explicitly producing a cross-path overview, run the full ICP process per product path and produce `research/{slug}/icp.md` per path plus a unified `research/icp.md`. If code clearly exposes a user-facing app without a matching product path, suggest creating `research/{slug}/` instead of treating monorepo detection as a gate.
   - **Migrate flat files when product paths are introduced:** If canonical flat `research/*.md` files exist and the user chooses or creates a product path, offer to move path-specific canonical docs into `research/{chosen-slug}/`. Leave or regenerate top-level files only when they are cross-path summaries.
   - **Migrate old convention:** If `research/icp-{slug}.md` files exist (old naming), offer to move them to `research/{slug}/icp.md` (and corresponding search logs to `research/{slug}/icp-search-log.md`). Create the subdirectories as needed.
2. **Broad market research**: WebSearch with 8–12 query strategies (personas, pain points, segments, trends, competitors, forums, job postings, industry reports, business model, willingness-to-pay signals). Log all queries and findings. **Classify the business model** into one or more of: B2B SaaS (PLG), B2B SaaS (SLG), B2C, B2C subscription, marketplace/platform, B2B2C, D2C, open-source/open-core, API/developer-first. Document classification with evidence in search log — this gates which sub-sections appear in the Discovery & Evaluation Behavior section.
3. **Identify 2–5 ICP candidates** from research evidence — note who they are, pain evidence, accessibility, value potential, and WTP signal strength.
4. **Checkpoint 1 — Present candidates to user.** Show ICP candidates with rationale — cite pain evidence found, accessibility signals, and value delivery reasoning from search findings for each candidate. Ask: "Do any surprise you? Any segment I'm missing?" Incorporate feedback before proceeding.
5. **Deep research per ICP**: Targeted WebSearch to fill the 9-section framework for each candidate:
   - **Customer Profile** — buyer persona, budget, discovery channels. Include **Geographic Focus** (only if the product has regulatory, language, or market-specific constraints — initial target region, why, expansion sequence), **Named Accounts** (B2B: 5–10 real companies that fit, with name, size, industry, and why they fit), and **Business Model & Go-to-Market Motion** (model type with evidence, primary motion PLG/SLG/community/partner/hybrid, buyer-user relationship)
   - **User Profile(s)** — daily users, sophistication, goals, frustrations
   - **Trigger Events** — what causes them to look NOW? Job changes, growth milestones, compliance deadlines, tool sunsets, contract renewals, funding events, new regulations. Rank by frequency and urgency.
   - **Current State Journey** — step-by-step current workflow
   - **Pain Map** — breakdowns, severity, frequency
   - **Current Alternatives (User Perspective)** — what users say they currently use or have tried, in their own words
   - **Market Sizing** — TAM/SAM/SOM via bottom-up (company counts × deal size) and top-down (industry reports, competitor revenue). Flag confidence level.
   - **Stated Value Drivers** — what customers say matters in their own language, the "aha moment" as they describe it. Include **Willingness-to-Pay Signals** as a bounded evidence subsection: paid alternatives, budget owner/context, current spend or time-cost proxy, switching-cost tolerance, economic urgency, and pricing sensitivity cues. Do not recommend prices, packages, or monetization strategy here.
   - **Customer ↔ User Dynamics** — post-purchase buyer-user relationship (provisioning, onboarding, admin vs end-user dynamics). For B2B, detailed buying process and DMU live in Discovery & Evaluation Behavior; this section focuses on the post-purchase relationship.
   - **Discovery & Evaluation Behavior** — how this persona found, evaluated, and chose solutions. Capture behavioural signals only (where they searched, who they asked, what they compared). Populate section 10.
6. **Checkpoint 2 — Present scoring matrix and primary ICP selection.** Show Value x Accessibility scores. The value rationale must explicitly distinguish pain intensity from WTP quality: active spend on alternatives, clear budget owner/context, high cost of inaction, tolerance for switching costs, and urgency tied to measurable economic outcomes count as strong WTP evidence; verbal interest without budget, free-only behavior, unclear owner, or price sensitivity that outweighs pain count as weak WTP evidence. Ask: "Which constraints, missing segments, or weak evidence should change this ranking?" Incorporate feedback.
7. **Cross-ICP analysis**: Shared pains, conflicts, product line recs, build sequence, lowest-hanging-fruit x most-value prioritization, discovery & evaluation comparison (how discovery and evaluation behavior differs across ICPs; do different ICPs find and choose solutions through different paths?).
   - Convert secondary ICPs, product-line recommendations, and materially different Cross-ICP Analysis outcomes into `research/.progress.yaml` `product_paths[]` entries when they imply a different product surface, product-path scope, audience-first path, or future pivot.
   - Manifest entries must include `id`, `label`, `source_skill: icp`, `scope_path`, `status`, `reason`, `archive_reason`, `archived_at`, `promoted_at`, `evidence_refs`, `revisit_trigger`, `next_skill`, `last_touched`, and `pipeline_stage: icp`.
   - Keep the selected primary ICP in `active_paths` by default. Recommend `$product-line activate` when secondary ICPs suggest a materially different product surface worth exploring again. Mark non-selected ICP/product paths `status: deferred` or `status: revisit_candidate`; do not run full competitive analysis, positioning, journey mapping, UX, or specs for every deferred path unless the user activates one.
8. **Checkpoint 3 — Present cross-ICP analysis and build sequence.** Show shared pains with source data, conflicts with specific examples, and build sequence rationale grounded in the scoring matrix. Ask: "Does this sequencing make sense?" Incorporate feedback.
9. **Final review**: Present complete findings summary. Ask: "Ready to write? Anything to adjust?" Only write after user confirms.

**After writing is complete, repeat the Recommended next step from the generated `## Next Steps` section in the final chat response.**

## Deliverables

- `research/icp.md` — Primary ICP in canonical 9 top-level `##` sections (Customer Profile, User Profile(s), Trigger Events, Current State Journey, Pain Map, Current Alternatives (User Perspective), Market Sizing, Stated Value Drivers, Customer ↔ User Dynamics). Include WTP evidence as a subsection inside `## Stated Value Drivers`, not as a new top-level parser-breaking section. Then supplementary `## Discovery & Evaluation Behavior` (section 10: how they find solutions, how they evaluate, how they choose), then `## Additional ICPs` (condensed 9-section + condensed discovery & evaluation per ICP, including condensed WTP evidence), then `## Cross-ICP Analysis` (prioritization matrix, shared pains, conflicts, product line recs, build sequence, discovery & evaluation comparison), then `## Signals for Downstream Research` (unvalidated observations routed to /competitive-analysis, /positioning, /monetization, /gtm)
- `research/icp-search-log.md` — Raw research log: every query, findings, evidence, scoring rationale
- `research/.progress.yaml` — product-path manifest when secondary ICPs, Cross-ICP Analysis, or product-line recommendations create parked or promotable paths. Status values include `active`, `deferred`, `archived`, `promoted`, and `revisit_candidate`.
- **Product-path or cross-path mode**: `research/{slug}/icp.md` + `research/{slug}/icp-search-log.md` per product path, plus unified `research/icp.md` cross-referencing all product-path ICPs with top-level prioritization when multiple active paths exist

The output file must end with a `## Next Steps` section based on which files exist. Include a **Recommended** item (the single highest-impact next step given current project state) with a one-line reason, followed by **Other options** (2–4 alternatives). Use this format in the output:

## Next Steps

**Recommended:** `$competitive-analysis` — maps the landscape your ICP operates in so positioning and GTM have competitive grounding

Other options:
- `$competitive-analysis` — Map the competitive landscape for this ICP's market (if no `research/competitive-analysis.md`)
- IF no `research/journey-map.md`: check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if `customer-lifecycle` is not enabled, recommend `$pack install customer-lifecycle` first; if `customer-lifecycle` is enabled, recommend `$journey-map` — map the current-state journey to find intervention points
- IF codebase exists: check `.agents/project.json.enabled_packs` for `business-ops` — if `business-ops` is not enabled, recommend `$pack install business-ops` first; if `business-ops` is enabled, recommend `$mvp-gap` — check if the codebase delivers on the ICP's top pain point
- IF `research/competitive-analysis.md` exists: check `.agents/project.json.enabled_packs` for `product-design` — if `product-design` is not enabled, recommend `$pack install product-design` first; if `product-design` is enabled, recommend `$brainstorm` — generate solution ideas grounded in the ICP research

Only include items whose conditions are met. The recommendation (`$competitive-analysis`) is always applicable.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Stay in problem space — do not propose features, architecture, or solutions.
- Evidence-based — every claim must trace to research logged in `research/icp-search-log.md`.
- Primary ICP must use canonical 9 `##` headers for downstream compatibility (`$spec-interview`, `$mvp-gap`, `$roadmap`, `$journey-map`). The renamed sections (`Current Alternatives (User Perspective)`, `Stated Value Drivers`) replace the former `Market Landscape` and `Value Proposition` headers. Section 10 (`## Discovery & Evaluation Behavior`) is supplementary and does not affect downstream parsing.
- Section 10 captures behavioural signals only — how personas find, evaluate, and choose solutions. Do not include GTM strategy, channel analysis, budget authority, procurement process, or pricing expectations — those belong in downstream skills (`$gtm`, `$monetization`, `$enterprise-icp`).
- WTP belongs in ICP only as evidence of segment fit and urgency: budget ownership, paid alternatives, current spend/time-cost proxies, switching-cost tolerance, economic urgency, and price sensitivity cues. Do not convert WTP evidence into pricing recommendations, packaging, discounting, ARPA targets, or monetization strategy; route those raw signals to `$monetization`.
- Minimum 8 WebSearch queries before identifying candidates, 2–3 per candidate after.
- Do not overwrite existing `research/icp.md` without asking.
- Present before writing — never write output until findings are validated through checkpoints.
- `## Next Steps` must be the final section in the output file, with a recommended next step and 2–4 other options.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/icp-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
