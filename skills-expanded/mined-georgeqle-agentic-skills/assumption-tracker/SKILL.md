---
name: assumption-tracker
description: Extract and risk-rank assumptions from research docs — living register of what to validate first
type: analysis
version: v0.1
argument-hint: "[optional: focus area e.g. \"pricing\", \"ICP\", \"channel\"]"
---

# Assumption Tracker — Riskiest Assumptions Register

Invoke as `$assumption-tracker`.

Scans all `research/*.md` files, extracts implicit and explicit assumptions, ranks by risk (catastrophic if wrong) × uncertainty (how little evidence), and produces a living register prioritizing what to validate first.

## Prerequisites

- **Hard**: At least 3 files must exist in `research/` (or `research/{app}/`). If fewer exist, tell the user to run more research skills first and stop.
- **Soft**: The more research docs exist, the more comprehensive the register. Reads all of: `research/icp.md`, `research/competitive-analysis.md`, `research/journey-map.md`, `research/metrics.md`, `research/gtm.md`, `research/monetization.md`, `research/customer-feedback.md`, `research/positioning.md`.

## Process

### 0. App Scope Resolution (Monorepo Support)

Before scanning, determine the app scope:

1. If `$ARGUMENTS` specifies an app name matching a subdirectory of `research/`, use it.
2. If `research/` contains subdirectories (excluding files), list them and ask the user which app to target. If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text. If only one subdirectory exists, use it automatically.
3. If no subdirectories exist, proceed with flat structure (single-product mode).

When app scope `{app}` is active:
- Read/write research from `research/{app}/` instead of `research/`

### 1. Load All Research

Read every `research/*.md` file (or `research/{app}/*.md`). For each document, extract:

- **Explicit claims** — statements presented as facts ("our ICP has budget authority", "the market is $2B")
- **Implicit assumptions** — unstated beliefs the analysis depends on ("users will switch from Excel", "word-of-mouth will be a growth channel", "the aha moment happens within 5 minutes")
- **Dependency assumptions** — where one research doc builds on conclusions from another ("GTM pricing assumes ICP willingness-to-pay from monetization research")

Track which document and section each assumption comes from.

### 2. Categorize Assumptions

Group assumptions into categories:

| Category | Examples |
|----------|----------|
| **ICP & Market** | Target segment exists, pain is severe enough to pay, market size estimates |
| **Value Proposition** | Our solution solves the pain, users prefer us over alternatives |
| **Pricing & Revenue** | Willingness to pay, price sensitivity, unit economics viability |
| **Channel & Distribution** | Can reach ICP through chosen channels, conversion rates, CAC assumptions |
| **Product & UX** | Users can achieve aha moment, activation flow works, retention drivers |
| **Competitive** | Competitor won't copy, switching costs exist, differentiation is durable |
| **Timing** | Market is ready now, no regulatory changes coming, technology is mature |

### 3. Score Each Assumption

For each assumption, score two dimensions:

**Risk (if wrong)** — 1 to 5:
- 1: Minor inconvenience, easy pivot
- 3: Significant rework needed, delays
- 5: Existential — business model collapses, wasted months of work

**Uncertainty (how little evidence)** — 1 to 5:
- 1: Strong evidence — multiple data points, validated by customer feedback
- 3: Moderate — some research supports it, but not validated with real users
- 5: Pure assumption — no evidence, taken on faith or "common sense"

**Combined priority** = Risk × Uncertainty (max 25). Higher = validate first.

### 4. Check Validation Status

Cross-reference assumptions against:
- `research/customer-feedback.md` — findings classified as "Confirmed" or "Wrong" may validate or invalidate assumptions
- `research/experiments/` directory — completed experiment results
- `research/cohort-review-*.md` — real performance data

Mark each assumption's validation status:
- **Unvalidated** — no evidence for or against
- **Partially validated** — some supporting evidence, not conclusive
- **Validated** — strong evidence confirms this assumption
- **Invalidated** — evidence contradicts this assumption
- **Stale** — was validated, but newer data raises questions

### 5. Present & Validate

Present the top 10 highest-priority assumptions to the user. If the session is already in Plan mode and there are 2-3 concrete validation choices, prefer `request_user_input`; otherwise ask in plain text:

- Show the assumption, source document, risk score, uncertainty score, combined priority, and validation status
- Ask: "Do these priorities feel right? Any assumptions I'm missing or scoring wrong?"
- Ask: "Are there any assumptions here you already know the answer to?"

Incorporate feedback before proceeding.

### 6. Generate Validation Recommendations

For each unvalidated high-priority assumption (combined score ≥ 12), recommend a validation method:

| Validation Method | Best For |
|-------------------|----------|
| `$experiment` — landing page test | Demand validation, messaging tests |
| `$experiment` — fake-door test | Feature demand, willingness to explore |
| `$experiment` — pricing test | Willingness to pay, price sensitivity |
| `$experiment` — survey | Broad sentiment, preference ranking |
| `$customer-feedback` — user interview | Deep understanding, "why" questions |
| `$cohort-review` — analyze real data | Post-launch metrics, funnel performance |
| Direct observation | UX assumptions, activation flow |
| Competitor analysis | Market timing, differentiation durability |

### 7. Populate Next Steps

Include 3–5 applicable items with "Pick one:" framing:

- IF unvalidated assumptions with score ≥ 15: `$experiment [top assumption]` — Design a cheap test for the riskiest assumption
- IF customer feedback exists but assumptions remain unvalidated: `$customer-feedback` — Gather targeted feedback on top assumptions
- IF product is live: `$cohort-review` — Check if real data validates or invalidates key assumptions
- IF assumptions cross multiple docs: `$reconcile-research` — Ensure research docs are internally consistent
- ALWAYS: `$research-roadmap` — Check overall project status

### 8. Write Output

Present final register to user. Ask:
- "Ready to write this to `research/assumption-tracker.md`? Anything to adjust first?"

Only after confirmation, write the output file.

## Output

### `research/assumption-tracker.md` (or `research/{app}/assumption-tracker.md`)

```markdown
# Assumption Tracker

> Last updated: [current date]
> Sources: [list of research docs scanned]
> Total assumptions: [count] | Unvalidated high-risk: [count]

## Summary

[2-3 sentences: the riskiest unvalidated assumptions and what to do about them]

## Top 10 Riskiest Assumptions

| # | Assumption | Source | Category | Risk | Uncertainty | Priority | Status |
|---|-----------|--------|----------|------|-------------|----------|--------|
| 1 | [assumption] | [doc:section] | [category] | [1-5] | [1-5] | [R×U] | [status] |
| ... | | | | | | | |

## Full Register

### ICP & Market
| Assumption | Source | Risk | Uncertainty | Priority | Status | Validation Method |
|-----------|--------|------|-------------|----------|--------|-------------------|
| [assumption] | [doc:section] | [1-5] | [1-5] | [R×U] | [status] | [method] |

### Value Proposition
[Same table format]

### Pricing & Revenue
[Same table format]

### Channel & Distribution
[Same table format]

### Product & UX
[Same table format]

### Competitive
[Same table format]

### Timing
[Same table format]

## Validation Plan

### Immediate (This Week)
[Top 1-3 assumptions to validate, with specific method and success criteria]

### Short-term (This Month)
[Next 3-5 assumptions, with recommended approach]

### Can Wait
[Lower-priority assumptions that don't block current decisions]

## Recently Validated / Invalidated

| Assumption | Previous Status | New Status | Evidence | Date |
|-----------|----------------|------------|----------|------|
| [assumption] | Unvalidated | Validated/Invalidated | [evidence source] | [date] |

## Next Steps

Pick one:
- [conditional items from step 7 — only include items whose conditions are met]
```

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Read-only on research docs.** Extract assumptions from existing research — do not modify source documents.
- **Be specific.** "Market exists" is not an assumption. "Solo creative professionals earning $50K-150K will pay $20/mo for portfolio analytics" is.
- **Trace to source.** Every assumption must reference the specific document and section it was extracted from.
- **Score honestly.** Don't inflate uncertainty to make things seem more urgent. If there's real evidence, score it low.
- **Update, don't duplicate.** If `research/assumption-tracker.md` already exists, ask the user whether to update (re-scan and merge) or overwrite. If the session is already in Plan mode and there are 2 concrete choices, prefer `request_user_input`. When updating, preserve validation status and "Recently Validated" history.
- **Present before writing.** Never write output files until findings have been presented and validated.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/assumption-tracker-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
