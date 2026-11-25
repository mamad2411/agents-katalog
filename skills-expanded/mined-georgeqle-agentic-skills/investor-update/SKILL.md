---
name: investor-update
description: Generate structured monthly stakeholder update from current research state, metrics, roadmap, and feedback
type: analysis
version: v0.3
argument-hint: "[optional: month e.g. \"March 2026\"]"
interview_depth: none
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Investor Update — Stakeholder Communication

Invoke as `$investor-update`.

Generates a structured monthly update from current research state, metrics, roadmap progress, and customer feedback. Uses standard YC/First Round format suitable for investors, accelerator mentors, or advisory boards.

## Soft Prerequisites

- Read all that exist: `research/metrics.md`, `research/cohort-review-*.md`, `research/runway-model.md`, `research/customer-feedback.md`, `research/gtm.md`, `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, `tasks/recurring-todo.md`, `tasks/history.md`
- The more data exists, the richer the update. Works with as little as a roadmap + basic metrics.

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

### 1. Load Context

Read all available data sources:
- **Metrics**: `research/metrics.md` for targets, `research/cohort-review-*.md` (most recent) for actuals
- **Financial**: `research/runway-model.md` for runway, burn, revenue
- **Customer**: `research/customer-feedback.md` for qualitative signal
- **Progress**: `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md` (if it exists), `tasks/history.md` for what was built; `tasks/record-todo.md` and `tasks/recurring-todo.md` for advisory measurements or cadence work that may affect asks/risks
- **GTM**: `research/gtm.md` for go-to-market context

Also check git log for the month to see what was shipped.

### 2. Compile Update Sections

For each section, pull from the appropriate data source. If a data source doesn't exist, either skip the section or ask the user for the data. If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`.

Fill gaps with user input. If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "What were the top 3 accomplishments this month?"
- "What's the #1 thing you need help with?"
- "Any key hires, partnerships, or milestones?"
- "What are you most worried about right now?"

### 3. Present & Validate

Show the complete update to the user before writing:
- "Here's the draft update. Does it accurately represent the month? Anything to add or change?"

Incorporate feedback before proceeding.

### 4. Write Output

Only after confirmation, write the output file.

## Output

### `research/investor-update-[YYYY-MM].md` (or `research/{slug}/investor-update-[YYYY-MM].md`)

```markdown
# Investor Update: [Month Year]

> Date: [current date]
> From: [product/company name]

## TL;DR
[2-3 sentences: the month in a nutshell — wins, challenges, and trajectory]

## Key Metrics

| Metric | Last Month | This Month | Target | Trend |
|--------|-----------|------------|--------|-------|
| [North Star] | [value] | [value] | [target] | [↑↓→] |
| MRR | [value] | [value] | [target] | [↑↓→] |
| Users | [value] | [value] | [target] | [↑↓→] |
| [Key metric] | [value] | [value] | [target] | [↑↓→] |

## Wins
1. [Accomplishment with impact — e.g., "Shipped X, resulting in Y"]
2. [Accomplishment]
3. [Accomplishment]

## Challenges
1. [Challenge and what you're doing about it]
2. [Challenge]

## Product
[What was built, shipped, or launched this month — concrete deliverables]

## Customers / Users
[New customers, notable feedback, retention signals, churn events]

## Financial
- **Cash**: $[amount]
- **Burn**: $[amount/mo]
- **Revenue**: $[MRR]
- **Runway**: [months]

## Plan for Next Month
1. [Top priority]
2. [Second priority]
3. [Third priority]

## Asks
[What you need help with — intros, advice, hiring, resources. Be specific.]

## Team
[Any changes — hires, departures, role changes]
```

Create the `research/` directory if it doesn't exist.

### Next Steps Guidance

The final response and output file must include a `## Next Steps` section with one explicit recommendation and 2-4 other options.

**Recommendation priority** (first applicable becomes the recommendation):

1. IF runway, burn, or revenue data is missing or stale: recommend `$runway-model` — investor updates need current financial context.
2. IF metrics are missing or stale: recommend `$metrics` — investor updates need a defensible KPI frame.
3. IF actual usage or retention data exists but has not been reviewed: recommend `$cohort-review` — convert operational data into investor-ready signal.
4. IF the update surfaced strategic misses, stale assumptions, or missed commitments: recommend `$retro` — turn the update into a corrective learning loop.
5. Otherwise recommend `$research-roadmap` — choose the next lifecycle task after the stakeholder update is current.

Use this format:

```markdown
## Next Steps

**Recommended:** [recommended skill] — [one-line reason grounded in the update]

Other options:
- [2-4 applicable alternatives]
```

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Honest and concise.** Investor updates should be transparent, not spin. Bad news delivered with a plan is better than hidden problems.
- **Present before writing.** Never write until the user validates the update.
- **Separate dated files.** Each update is a new file. Don't modify previous updates.
- **No fabrication.** Only include metrics that have real data behind them. If a metric isn't tracked yet, omit it rather than estimate.
- **Standard format.** Stick to the YC/First Round format — investors expect this structure.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/investor-update-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
