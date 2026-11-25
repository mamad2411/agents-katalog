---
name: competitive-analysis
description: Research competitors via web search — map the landscape, GTM strategies, strengths, weaknesses, and market gaps
type: research
version: v0.9
argument-hint: "[concept | optional: product category or specific competitors to investigate]"
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Competitive Analysis — Market Landscape Research

## Report-First Approval Gate

Default to report-only: present findings, evidence coverage, assumptions, recommended artifact path, and proposed file changes in a pre-approval alignment page plus a concise conversation summary for user approval before creating or updating canonical research, spec, or task files.

Do not write or overwrite synthesized deliverables until the user explicitly approves, unless the user invoked an explicit write/update/fix mode or clearly asked to write files upfront. Raw evidence capture may be persisted before analysis when reproducibility requires it; report those raw paths separately and still gate synthesized research/report writes.

When stopping for approval, build and attempt to open the alignment preview page first, then ask the user to review it and approve, question, or request adjustments. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

Conduct deep web-based research to compile a comprehensive competitive landscape for the project. Uses web search to identify competitors, evaluate their maturity, analyse their go-to-market strategies, and surface market gaps.

Default stance: assume the user has no insider knowledge of the market. Present the landscape, category terms, and recommendations from first principles so the analysis stands on its own. Ask for corrections, hard constraints, or proprietary facts, not intuition.

## Prerequisites

**Detect mode before proceeding:**

- **Concept-validation mode** activates when: no `research/icp.md` AND (no meaningful codebase OR `$ARGUMENTS` contains "concept"/"validate"). Use this mode to validate market gaps after a concept has been shaped by `$idea-scope-brief` or an equivalent brief; if no concept is clear, recommend `$idea-scope-brief` first. Announce mode to user, then ask for concept description (problem, audience, approach).
- **Standard mode** (default): Read the codebase, README, CLAUDE.md, and existing research/specs (`research/icp.md` or `research/{app}/icp.md`, `research/enterprise-icp.md` or `research/{app}/enterprise-icp.md`, `research/mvp-gap.md` or `research/{app}/mvp-gap.md`) to understand the product.
- Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading. In standard mode, scope the full competitive analysis to the first entry in `active_paths` by default. Treat `product_paths[]` entries with `status: deferred` or `status: revisit_candidate` as parked product paths, not as extra full research tracks.

## Process

### 0. App Scope Resolution (Monorepo Support)

Before checking prerequisites, determine the app scope:

1. If `$ARGUMENTS` specifies an app name matching a subdirectory of `research/`, use it.
2. If `research/` contains subdirectories (excluding files), list them and ask the user which app to target. If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text. If only one subdirectory exists, use it automatically.
3. If no subdirectories exist, proceed with flat structure (single-product mode).

When app scope `{app}` is active:
- Read/write research from `research/{app}/` instead of `research/`
- Read/write specs from `specs/{app}/` instead of `specs/`
- Also read `research/icp.md` (cross-app overview) for broader context

### 1. Establish Product Context

**Standard mode:** Read CLAUDE.md, README, package config, key source files. Read `research/icp.md` (or `research/{app}/icp.md`) if it exists — the ICP defines the competitive frame. Read `research/enterprise-icp.md` (or `research/{app}/enterprise-icp.md`) and `research/mvp-gap.md` (or `research/{app}/mvp-gap.md`) if they exist. Summarise what the product does, who it's for, and what problem it solves.

**Concept-validation mode:** Use `research/concept-brief.md` when present, otherwise use the concept description from Prerequisites. Summarise what the concept proposes (problem, audience, approach). Confirm with the user before researching.

### 2. Identify Competitors

Use web search extensively across: direct competitors, indirect competitors, incumbents, emerging players, DIY alternatives.

**Checkpoint 1 — Present competitor list to user.** Show all identified competitors grouped by category. For each competitor, include a one-line description and why it's in that category, citing the search source. Ask: "Are there competitors I missed? Any incorrectly categorised?" Incorporate feedback.

### 3. Research Each Competitor

For each: Company & Product (features, funding, pricing), Maturity & Traction (stage, user signals, integrations), GTM Strategy (acquisition, pricing, content, community), Strengths (user praise, moat), Weaknesses (complaints, gaps, vulnerabilities).

### 4. Identify Market Gaps & White Space

Synthesise gaps and white-space opportunities: underserved segments, feature gaps, pricing gaps, UX gaps, integration gaps, geographic/vertical gaps, technology gaps.

**Standard mode additional synthesis:** 2-3 most significant white-space opportunities, competitor lessons (do's and don'ts).

When evidence materially affects parked product paths from `research/.progress.yaml`, add a short `## Implications for Deferred Product Paths` section summarizing the impact, evidence refs, and whether the `revisit_trigger` should change. Do not broaden standard mode into full competitive analysis for every deferred path unless the user explicitly promotes one. When competitive gaps imply an entirely new product surface not covered by existing product paths, recommend `$product-line fork` to create a new path entry.

**Concept-validation mode additional synthesis:** Frame as hypothetical — segments the concept could serve that competitors miss, capability gaps, competitor lessons. Positioning recommendations belong in `$positioning`.

### 4a. Gap Assessment (concept-validation mode only)

Synthesise market gaps into: **Market State** (Virgin/Sparse/Crowded), **Incumbent Quality** (Dominant-and-loved / Dominant-but-resented / Fragmented-and-mediocre / Emerging-and-unproven), **Gap Quality** (Clear unmet need / Underserved segment / UX/approach gap / Minor improvement / No meaningful gap), **Verdict** (Proceed to ICP / Pivot concept / Abandon). If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text before continuing.

### 5. Present Findings & Validate

**Checkpoint 2 — Present full analysis before writing.** Show: landscape summary, key competitors, market gaps and white-space opportunities, observable GTM patterns, lessons from competitors. Ask: "Which gaps or assumptions need stronger evidence? Any gaps I missed or got wrong?" Continue until all details are nailed down.

### 6. Write Output

Only after user validates, write the output files.

## Deliverables

- `research/competitive-analysis.md` (or `research/{app}/competitive-analysis.md`) — Full competitive landscape: summary, competitor profiles, observable GTM patterns, market gaps, competitive positioning (gaps identified, lessons), signals for downstream research, next steps. In concept-validation mode, includes `## Gap Assessment` section (Market State, Incumbent Quality, Gap Quality, Verdict).
- `research/competitive-analysis-search-log.md` (or `research/{app}/competitive-analysis-search-log.md`) — Raw research log: every query, findings, source attribution, reasoning
- `research/.progress.yaml` — update only when active-path evidence changes a deferred product path's status, reason, evidence refs, revisit trigger, or next skill. Use `product_paths` terminology instead of branch terminology. When writing manifest entries, include `pipeline_stage: competitive-analysis` on the active path entry.

**Standard mode next steps:** `## Next Steps` section with a **Recommended** item and **Other options** (2–4 alternatives). Choose the recommended item by the first matching condition:

1. IF no `research/journey-map.md`: check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if `customer-lifecycle` is not enabled, recommend `$pack install customer-lifecycle` first; if `customer-lifecycle` is enabled, recommend `$journey-map` — map the customer and user journey before solution-value decisions, using competitive gaps as inspiration
2. IF no `research/positioning.md`: `$positioning` — frame the market category and alternatives after journey evidence shows where value is delivered
3. IF no `specs/ux-variations-*.md`: check `.agents/project.json.enabled_packs` for `product-design` — if `product-design` is not enabled, recommend `$pack install product-design` first; if `product-design` is enabled, recommend `$ux-variations [top journey-backed market gap or positioning opportunity]` — explore experience directions before production specification
4. IF no `research/value-prop.md` AND solution-customer fit is weak, disputed, or needs explicit fit scoring: `$value-prop-canvas` — validate contested solution-fit evidence as an optional detour
5. IF no `research/gtm.md`: check `.agents/project.json.enabled_packs` for `business-growth` — if `business-growth` is not enabled, recommend `$pack install business-growth` first; if `business-growth` is enabled, recommend `$gtm` — build go-to-market plan leveraging competitive gaps
6. IF codebase exists and no `research/mvp-gap.md`: check `.agents/project.json.enabled_packs` for `business-ops` — if `business-ops` is not enabled, recommend `$pack install business-ops` first; if `business-ops` is enabled, recommend `$mvp-gap` — check if the codebase exploits the gaps found

Use this format in the output:

## Next Steps

**Recommended:** `[first matching command above]` — [reason grounded in this analysis]

Other options:
- `$pack install customer-lifecycle` or `$journey-map` — map the customer journey to find where competitors fall short (if no `research/journey-map.md` and not recommended; check `.agents/project.json.enabled_packs` for `customer-lifecycle` — if not enabled, recommend `$pack install customer-lifecycle`; if enabled, recommend `$journey-map`)
- `$positioning` — frame the market category and competitive alternatives after journey evidence exists (if no `research/positioning.md` and not recommended)
- check `.agents/project.json.enabled_packs` for `product-design` — if `product-design` is not enabled, recommend `$pack install product-design` first; if `product-design` is enabled, recommend `$ux-variations [top journey-backed market gap or positioning opportunity]` — explore prototype directions before production specification (if positioning exists and not recommended)
- `$value-prop-canvas` — optional detour only when solution-customer fit is weak, disputed, or needs explicit fit scoring before positioning/spec work
- check `.agents/project.json.enabled_packs` for `business-growth` — if `business-growth` is not enabled, recommend `$pack install business-growth` first; if `business-growth` is enabled, recommend `$gtm` — build go-to-market plan leveraging competitive gaps (if no `research/gtm.md` and not recommended)
- check `.agents/project.json.enabled_packs` for `business-ops` — if `business-ops` is not enabled, recommend `$pack install business-ops` first; if `business-ops` is enabled, recommend `$mvp-gap` — check if the codebase exploits the gaps found (if codebase exists, no `research/mvp-gap.md` exists, and not recommended)
- check `.agents/project.json.enabled_packs` for `product-design` — if `product-design` is not enabled, recommend `$pack install product-design` first; if `product-design` is enabled, recommend `$brainstorm` — generate alternative solution ideas (only if the analysis found multiple plausible market gaps and product direction is still unclear)

Only include items whose conditions are met. Do not recommend brainstorm just because competitive whitespace exists.

**Concept-validation mode next steps:** Use the same Recommended + Other options format, but choose the recommendation from the validated `## Gap Assessment` verdict:

## Next Steps

**Recommended:** [verdict-based next step] — [reason grounded in the gap assessment]

Other options:
- IF verdict is **Proceed to ICP**: recommend `$icp` — the competitive gap is validated; define who to build for
- IF verdict is **Pivot concept**: recommend `$brainstorm` — the market has a gap, but this concept needs a different angle before ICP work is useful
- IF verdict is **Abandon**: recommend `No follow-up skill recommended` — the analysis did not find a meaningful gap worth pursuing; include `$brainstorm` only if the user wants to explore a new concept
- `$competitive-analysis` — re-run in standard mode after ICP is defined (only after a proceed verdict and after `$icp` creates `research/icp.md`)

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Use web search extensively — every competitor must come from a search result.
- Cite sources for competitor facts.
- Be honest about uncertainty.
- Stay in analysis mode — no product changes, architecture, or positioning recommendations. Positioning belongs in `$positioning`.
- Focus on actionable insights over raw lists.
- Do not overwrite existing `research/competitive-analysis.md` (or `research/{app}/competitive-analysis.md`) without asking.
- Prefer recent sources (last 12 months).
- Search breadth over depth initially.
- Present before writing — never write until findings are validated.
- `## Next Steps` must be the final section in the output file, with a recommended next step and 2–4 other options.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/competitive-analysis-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
