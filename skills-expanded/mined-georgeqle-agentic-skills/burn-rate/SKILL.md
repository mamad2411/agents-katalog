---
name: burn-rate
description: "Estimate monthly burn rate from infrastructure signals and calculate payback period against revenue projections"
type: analysis
version: v0.4
interview_depth: light
visual_tier: visual
---

# Burn Rate — Infrastructure-Grounded Cost & Runway Analysis

Invoke as `$burn-rate`.

Analyzes infrastructure, third-party services, and team costs to estimate monthly burn rate, then calculates payback period and break-even against revenue projections. Bridges `$monetization` (unit economics) and `$scale-audit` (infrastructure readiness) with dollar-denominated cost projections.

Default stance: assume the user does not know infrastructure pricing or SaaS cost structure in detail. Cost estimates must stand on detected services, cited pricing research, and explicit assumptions before asking the user for missing internal numbers.

## Prerequisites

- **Hard**: None — can run on any codebase.
- **Soft**: Read if they exist — `research/monetization.md`, `research/metrics.md`, `research/gtm.md`, `research/icp.md`, `CLAUDE.md`, `README`.

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

### 1. Load Context & Detect Costs

1. Read infrastructure files — containers, IaC, k8s, CI/CD, serverless, PaaS, cloud configs.
2. Read dependency files for third-party service SDKs (payments, auth, monitoring, AI/ML, email, search, etc.).
3. Read environment templates (`.env.example`, etc.) for API keys implying paid services.
4. Read existing research docs for revenue projections, unit economics, customer counts.
5. Build a cost inventory across: **Compute**, **Database**, **Storage**, **Third-party services**, **CI/CD**, **DNS/Domain**.
6. For each detected service: search current pricing (min 4 queries), estimate monthly cost, note assumptions, assign confidence (High/Medium/Low).

### 2. Interview — Fill Gaps

Ask 2-3 focused questions:
- Present detected infrastructure with estimated costs and cited pricing assumptions. Ask the user to correct factual inaccuracies or add missing internal costs, not to estimate from intuition.
- Ask about team size, fully-loaded cost per person, and non-infra costs (marketing, tools, legal).
- If revenue data not found in research docs, ask for current or projected MRR and cash on hand.

### 3. Calculate & Present

Compute with all assumptions visible:
- **Monthly Burn Rate** — infrastructure + team + other, broken down by category with percentages.
- **Runway** — cash on hand / monthly burn (only if cash position provided).
- **Payback Period** — total investment / monthly net revenue (or "N/A — pre-revenue").
- **Break-even Point** — three scenarios (conservative 50%, base, optimistic 150% growth). Skip if pre-revenue with no projections.
- **Cost per Customer** — infrastructure and total cost per customer (only if count known).
- **Cost Optimization Opportunities** — over-provisioned resources, cheaper alternatives, free tier headroom, reserved discounts.

Present analysis and ask for factual corrections, missing internal figures, or hard constraints before writing.

### 4. Downstream Impact & Next Steps

1. Check if `research/monetization.md` exists and conflicts with burn rate findings (stale margins, divergent unit economics). Classify as None/Minor/Major.
2. Populate `## Next Steps` (3-5 items, "Pick one:" framing) — conditionally suggest the following based on what exists and what conflicts were found:
   - `$scale-audit` — same pack, always valid
   - `$reconcile-research` — same pack, always valid
   - IF no `research/monetization.md`: check `.agents/project.json.enabled_packs` for `business-growth` — if `business-growth` is not enabled, recommend `$pack install business-growth` inside Codex, or `npx skillpacks install business-growth` from the project shell, first; if `business-growth` is enabled, recommend `$monetization` — Build pricing strategy informed by actual infrastructure costs
   - IF `research/monetization.md` exists but unit economics differ: check `.agents/project.json.enabled_packs` for `business-growth` — if `business-growth` is not enabled, recommend `$pack install business-growth` inside Codex, or `npx skillpacks install business-growth` from the project shell, first; if `business-growth` is enabled, recommend `$monetization` — Update unit economics with infrastructure-grounded costs
   - IF no `research/gtm.md`: check `.agents/project.json.enabled_packs` for `business-growth` — if `business-growth` is not enabled, recommend `$pack install business-growth` inside Codex, or `npx skillpacks install business-growth` from the project shell, first; if `business-growth` is enabled, recommend `$gtm` — Build go-to-market plan with cost-aware pricing
   - IF no `research/metrics.md`: check `.agents/project.json.enabled_packs` for `business-growth` — if `business-growth` is not enabled, recommend `$pack install business-growth` inside Codex, or `npx skillpacks install business-growth` from the project shell, first; if `business-growth` is enabled, recommend `$metrics` — Define metrics to track burn rate health (cost per customer, infrastructure efficiency)
   - IF codebase exists and optimization opportunities found: check `.agents/project.json.enabled_packs` for `product-design` — if `product-design` is not enabled, recommend `$pack install product-design` inside Codex, or `npx skillpacks install product-design` from the project shell, first; if `product-design` is enabled, recommend `$brainstorm` — Explore cost optimization as a feature priority

## Deliverables

- `research/burn-rate.md` (or `research/{slug}/burn-rate.md`) — Full analysis: infrastructure cost breakdown, team/operational costs, total burn rate, revenue projections, payback/break-even scenarios, runway, cost per customer, optimization opportunities, assumptions, downstream impact, and next steps.
- `research/burn-rate-interview.md` (or `research/{slug}/burn-rate-interview.md`) — Raw interview log with detected infrastructure, questions, responses, and key figures.

Create the `research/` (or `research/{slug}/`) directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Every cost estimate must trace to a detected service or user-provided figure.
- State all assumptions (tier, instance size, usage level) with confidence levels.
- Present full analysis to user before writing output files.
- Do not overwrite existing `research/burn-rate.md` without asking.
- Minimum 4 web search queries for pricing data before presenting estimates.
- Do not prescribe architecture changes — note optimization opportunities only.
- Do not contradict existing `research/monetization.md` — reconcile differences.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/burn-rate-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
