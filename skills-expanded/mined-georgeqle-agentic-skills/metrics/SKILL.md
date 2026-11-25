---
name: metrics
description: Define success metrics framework — activation, engagement, retention, growth, and business metrics tied to journey stages
type: analysis
version: v0.4
argument-hint: "[optional: focus area e.g. \"activation\", \"retention\"]"
interview_depth: full
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Metrics — Success Metrics Framework

Invoke as `$metrics`.

Research-first skill that defines measurable success metrics tied to journey stages. Each metric gets a definition, measurement method, target with rationale, and instrumentation requirements.

## Prerequisites

- **Hard**: `research/journey-map.md` (or `research/{slug}/journey-map.md` in product-path mode) must exist. If not, tell the user to run `$journey-map` first and stop.
- **Soft**: Read `research/icp.md` (or `research/{slug}/icp.md`) and `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`) if they exist — these improve target-setting and relevance.

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

### 1. Product Path Manifest

Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope the metrics framework to the active product path by default. When defining metrics that would only be relevant to a deferred product path, note the finding in a `## Product Path Implications` section.

### 2. Load Context

- Read `research/journey-map.md` (or `research/{slug}/journey-map.md`) — customer journey stages, aha moment, habit loop, churn triggers, critical moments
- Read `research/icp.md` (or `research/{slug}/icp.md`) if it exists — ICP segments, pain points, value props
- Read `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`) if it exists — real user behavior patterns, validated/invalidated assumptions
- Read CLAUDE.md and README if they exist — product context and tech stack (affects instrumentation)
- Read key source files if a codebase exists — understand what can actually be measured today

### 3. Interview

Codex interview cadence is one primary decision question per turn by default. Use short follow-up bullets only when they clarify the same metrics decision, not to batch unrelated questions. If the session is already in Plan mode, `request_user_input` may present 2-3 concrete choices for the current decision; otherwise ask one concise plain-text question.

**Research and recommend by default.** For each decision point, use web search, upstream research docs (`research/*.md`), and codebase analysis to gather evidence before asking the user. Assume the user has no insider knowledge unless they explicitly provide it. Present findings with data, define any relevant terms, state a recommendation with reasoning, and ask the user to approve, adjust, or override based on hard constraints, proprietary facts, or corrections. Only ask the user to choose without a recommendation when the decision genuinely depends on internal constraints, personal preferences, or strategic bets that cannot be inferred from evidence.

Cover these metric categories (skip or abbreviate areas the user has already addressed in `$ARGUMENTS`):

#### A. Activation Metrics
Tied to the **aha moment** from the journey map.
- What specific action signals that a user "gets it"? (the aha moment)
- How quickly should this happen after signup? (time-to-value target)
- What's the activation rate target? (% of signups who reach aha)
- Can this be measured today, or does instrumentation need to be built?

#### B. Engagement Metrics
Tied to the **habit loop** from the journey map.
- What does a "healthy" usage pattern look like? (daily/weekly/monthly, duration, depth)
- What's the core action that engaged users do repeatedly?
- What frequency indicates strong engagement vs. at-risk?
- Are there different engagement patterns by user profile?

#### C. Retention Metrics
Tied to **churn triggers** from the journey map.
- What defines retention? (still active after 7/30/90 days? Still paying?)
- What are the leading indicators of churn? (from journey map churn triggers)
- What's the target retention rate? By what timeframe?
- What's the current retention baseline (if any data exists)?

#### D. Growth Metrics
Tied to **expansion and advocacy** from the journey map.
- How do new users discover the product? (from journey map discovery channels)
- Is there a viral loop? What's the viral coefficient target?
- What expansion metrics matter? (seats added, usage increased, tier upgraded)
- What's the target growth rate? (week-over-week, month-over-month)

#### E. Business Metrics
Revenue, unit economics, sustainability.
- What's the revenue model? (from GTM if it exists, otherwise ask)
- What's the CAC target? (customer acquisition cost)
- What's the LTV target? (lifetime value)
- What's the LTV:CAC ratio target?
- What's the payback period target?

### 4. Present Findings & Validate

**Present the complete metrics framework to the user before writing.** Summarise:
1. Overview — the 5-8 key metrics and how they connect to journey stages
2. Each metric with definition, target (citing rationale: benchmarks, journey data, or ICP signals that informed the target), and measurement method
3. Instrumentation gaps — what can't be measured today
4. The "North Star" metric — the single metric that best captures overall health, with evidence for why this metric was chosen over alternatives

If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "Does this metrics framework capture success clearly? Which targets, assumptions, or instrumentation gaps should I revise?"

Continue until the user confirms. Only then proceed to writing.

### 5. Populate Next Steps

Before writing, check which files exist to populate the `## Next Steps` section contextually. Include a **Recommended** item (the single highest-impact next step given current project state) with a one-line reason, followed by **Other options** (2-4 alternatives). Choose the recommendation by the first matching condition:

Use this format in the output:

```markdown
## Next Steps

**Recommended:** [recommended skill] — [one-line reason grounded in this metrics framework]

Other options:
- [2-4 applicable alternatives]
```

- IF instrumentation gaps and no specs for them: `$roadmap` — Sequence instrumentation for the top metric gap into the roadmap
- IF no `tasks/roadmap.md`: `$roadmap` — Plan the build with instrumentation phases
- IF no `research/gtm.md`: `$gtm` — Build a GTM plan — metrics define what launch success looks like
- IF `tasks/roadmap.md` exists: `$exec` — Start building and instrumenting
- IF product is live and no `research/customer-feedback.md`: `$customer-feedback` — Collect data to validate metric targets
- IF product is live and real data exists: `$cohort-review` — Analyze actual performance against these targets
- IF a baseline measurement depends on future production data or aggregate access and is not a launch gate: add it to `tasks/record-todo.md`, not `tasks/todo.md` or `tasks/manual-todo.md`

**Impact-aware adjustments:**
- IF downstream impact is **Major**: prepend `$reconcile-research — [N] conflicts found in downstream docs` as the first item
- IF downstream impact is **Minor**: annotate relevant skill suggestions with "(stale — [brief description])"
- If downstream impact has not been classified yet, run the downstream impact check against the proposed output before selecting the final recommendation. Do not emit a Minor/Major impact recommendation speculatively.

### 6. Write Output

Only after the user has validated the findings, write the output files.

### 7. Downstream Impact Check

After writing, check for downstream research documents that may be affected by what was just decided. Only check documents that exist on disk.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/monetization.md`

For each existing downstream document:
1. Read it — focus on `> Based on:` header, `## Summary`, and sections that reference concepts this skill just defined or changed
2. Identify **specific conflicts**: claims, assumptions, or references that contradict what was just decided. Examples:
   - Metric targets or definitions referenced in monetization that no longer match
   - Revenue model assumptions anchored to metrics that changed
   - Conversion or retention targets that have shifted
3. Note each conflict: downstream file, section, the stale claim (quote it), and what it should now say

**Classify the impact**:
- **None**: No downstream documents exist, or no conflicts found. Skip display entirely.
- **Minor** (1–2 small conflicts): Display conflicts to user inline.
- **Major** (3+ conflicts OR a foundational assumption changed — e.g., North Star metric changed, activation definition redefined, retention targets shifted significantly): Display conflicts and strongly recommend `$reconcile-research`.

Display to the user after showing the written file confirmation. This should be quick — one read per downstream doc, scan for conflicts against key decisions. Not a deep reconciliation.

## Output

### `research/metrics.md` (or `research/{slug}/metrics.md`)

```markdown
# Success Metrics Framework

> Based on: research/journey-map.md (or research/{slug}/journey-map.md)[, research/icp.md, research/customer-feedback.md]
> Date: [current date]

## Summary
[2-3 sentences: the North Star metric, key health indicators, and biggest instrumentation gap]

## North Star Metric
**Metric**: [name]
**Definition**: [precise definition]
**Why this metric**: [how it captures overall product health]
**Target**: [specific number with timeframe]
**Current**: [baseline if known, or "not yet measured"]

## Activation

### [Metric Name]
**Definition**: [precise, unambiguous definition]
**Journey tie-in**: [which journey stage/moment this measures — reference journey-map.md]
**Measurement**: [how to measure — event, query, or manual process]
**Target**: [specific number] — [rationale for this target]
**Instrumentation**: [what needs to exist to measure this]
**Status**: [measurable today / needs instrumentation / needs design]

[Repeat for each activation metric]

## Engagement

### [Metric Name]
**Definition**: [precise definition]
**Journey tie-in**: [which habit loop or core action this tracks]
**Measurement**: [how to measure]
**Target**: [specific number] — [rationale]
**Instrumentation**: [what's needed]
**Status**: [measurable / needs work]

[Repeat for each engagement metric]

## Retention

### [Metric Name]
**Definition**: [precise definition]
**Journey tie-in**: [which churn trigger this monitors]
**Measurement**: [how to measure]
**Target**: [specific number] — [rationale]
**Instrumentation**: [what's needed]
**Status**: [measurable / needs work]

[Repeat for each retention metric]

## Growth

### [Metric Name]
**Definition**: [precise definition]
**Journey tie-in**: [which expansion/advocacy path this tracks]
**Measurement**: [how to measure]
**Target**: [specific number] — [rationale]
**Instrumentation**: [what's needed]
**Status**: [measurable / needs work]

## Business

### [Metric Name]
**Definition**: [precise definition]
**Measurement**: [how to measure]
**Target**: [specific number] — [rationale]
**Status**: [measurable / needs work]

[Repeat for each business metric]

## Instrumentation Gaps

| Metric | What's Missing | Effort | Priority |
|--------|---------------|--------|----------|
| [metric] | [what needs to be built] | S/M/L | [High/Med/Low] |

_Start with:_ `$roadmap` — Sequence instrumentation for the top metric gap into the roadmap.

## Metric Dependencies
[How metrics relate to each other — e.g., activation drives retention, retention drives LTV. Identify which metrics are leading vs. lagging indicators.]

<!-- Only include this section when downstream impact is Minor or Major. Omit entirely for None. -->
## Downstream Impact

> Checked: [list of downstream docs checked]
> Impact: Minor | Major

### Conflicts Found

1. **research/[file].md** — [Section Name]
   - **Stale**: "[exact quote from downstream doc]"
   - **Now**: [what this skill's output says instead]

[For Major only:]
> **Recommended action**: Run `$reconcile-research` to audit and fix all affected downstream documents.

## Next Steps

**Recommended:** [recommended next step] — [one-line reason grounded in this artifact]

Other options:
- [conditional items from step 4 — only include items whose conditions are met]
```

### `research/metrics-interview.md` (or `research/{slug}/metrics-interview.md`)
Raw interview log — questions, options presented, user responses, and a closing summary of key decisions.

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Requires journey map.** Metrics must be tied to actual journey stages, not abstract business goals.
- **Be precise.** "User engagement" is not a metric. "Weekly active users who complete at least 3 [core action] per week" is.
- **Include instrumentation.** Every metric must specify how to measure it and whether that measurement exists today.
- **Present before writing.** Never write output files until the framework has been presented and validated.
- **Tie to journey stages.** Every non-business metric must reference a specific stage or moment from the journey map.
- **Do not overwrite existing `research/metrics.md`** (or `research/{slug}/metrics.md`) without asking the user first.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/metrics-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
