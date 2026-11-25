---
name: experiment
description: Design lean validation experiments — hypothesis, method, success criteria, sample size, timeline, and decision rules
type: planning
version: v0.6
argument-hint: <hypothesis or assumption to test>
interview_depth: light
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Experiment — Lean Validation Design

Takes a hypothesis (from `$assumption-tracker` or user) and designs a cheap, fast validation experiment. Covers landing page tests, fake-door tests, concierge MVPs, surveys, A/B tests, pricing tests, and smoke tests. Outputs a structured plan with hypothesis, method, success criteria, sample size, timeline, and decision rules.

## Soft Prerequisites

- Read `research/assumption-tracker.md` if it exists — pulls the highest-priority unvalidated assumption
- Read `research/icp.md` if it exists — grounds experiment design in who the target is
- Read `research/metrics.md` if it exists — aligns success criteria with existing metric definitions
- Read `research/gtm.md` if it exists — leverages channel strategy for reaching test subjects

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

Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope experiment design to the active product path by default. When experiment results validate or invalidate assumptions about a deferred product path, add a `## Product Path Implications` section recommending `$product-line activate` or `$product-line archive` as appropriate.

### 2. Parse Input & Load Context

**Read `$ARGUMENTS`:**
- If it's a specific hypothesis or assumption: use it directly
- If it's a reference to an assumption number (e.g., "#3"): look it up in `research/assumption-tracker.md`
- If empty: check `research/assumption-tracker.md` for the highest-priority unvalidated assumption. If no tracker exists, ask the user what they want to test. If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`.

**Load context:** Read available research docs to understand the ICP, channels, metrics, and existing knowledge.

### 3. Structure the Hypothesis

Convert the input into a structured hypothesis:

**Format**: "We believe that [target segment] will [expected behavior] because [rationale]. We'll know this is true when [measurable outcome]."

Present and refine with the user. If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Here's how I've structured the hypothesis. Does this capture what you want to test?"
- If the hypothesis is too broad, help narrow it to something testable in 1-2 weeks

### 4. Research Experiment Methods

Use WebSearch with **3-5 targeted queries** to find best practices for this type of validation:

1. **Method-specific** — "[experiment type] validation method", "how to test [hypothesis type]"
2. **Sample size** — "[experiment type] sample size calculator", "minimum viable test size"
3. **Benchmarks** — "[category] conversion rate benchmark", "[experiment type] typical results"
4. **Tools** — "[experiment type] tools", "cheapest way to test [hypothesis]"

### 5. Design the Experiment — Present & Validate

Select the most appropriate experiment type and design the full plan:

#### Experiment Types

| Type | Best For | Timeline | Cost |
|------|----------|----------|------|
| **Landing page test** | Demand validation, messaging | 1-2 weeks | $50-200 (ads) |
| **Fake-door test** | Feature demand, willingness to explore | 1 week | $0 (in-product) |
| **Concierge MVP** | Value delivery, willingness to pay | 2-4 weeks | Time only |
| **Survey** | Broad sentiment, preference ranking | 3-5 days | $0-100 |
| **A/B test** | Optimization, messaging variants | 1-2 weeks | $0 (in-product) |
| **Pricing test** | Willingness to pay, price sensitivity | 1-2 weeks | $50-200 |
| **Smoke test** | Demand for non-existent feature | 3-5 days | $0-50 |
| **Pre-sale / LOI** | B2B willingness to pay | 1-2 weeks | Time only |
| **Wizard of Oz** | Complex feature viability | 2-4 weeks | Time only |

**Present the experiment design to the user.** If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text. Show:
- Recommended experiment type with rationale (why this method over alternatives)
- Detailed plan with timeline and cost estimate
- Success criteria with specific numbers (citing benchmarks from research)
- Decision rules for both outcomes

Ask:
- "Does this experiment design feel feasible? Too ambitious or too simple?"
- "Any resource constraints I should know about? (budget, time, access to users)"

Incorporate feedback before proceeding.

### 6. Define Decision Rules

For each possible outcome, define what happens next:

- **If hypothesis is validated** (success criteria met): What's the next step? (e.g., build the feature, commit to the pricing, double down on the channel)
- **If hypothesis is invalidated** (criteria not met): What's the pivot? (e.g., test alternative, revisit ICP, change approach)
- **If results are inconclusive** (between thresholds): What additional data is needed? Run a follow-up experiment or extend the current one?

### 7. Populate Next Steps

Include a **Recommended** item for the current design-stage next step, followed by **Other options**. Separate current next steps from outcome-specific next steps:

Use this format in the output:

```markdown
## Next Steps

**Recommended:** Run the experiment — the plan is only useful after the evidence is collected

Other options:
- [2-4 applicable alternatives]
```

- ALWAYS: Run the experiment (manual step — the plan tells you how)
- For a newly designed experiment, do not list validation/invalidation commands as current top-level next steps; put those under `## Decision Rules` because they are only valid after results exist.
- In `### If Validated`: include the next valid command, usually `$customer-feedback [results]` to log evidence, `$assumption-tracker` to mark the assumption validated, or `$roadmap` if the result commits the team to build.
- In `### If Invalidated`: include `$assumption-tracker` to mark the assumption invalidated, plus `$brainstorm`, `$customer-discovery`, `$gtm`, or `$monetization` only when the failed assumption belongs to that domain.
- In `### If Inconclusive`: include `$experiment [follow-up]` if the test needs another run, or `$customer-feedback` if qualitative evidence is the missing signal.
- IF more assumptions remain untested after this design: `$experiment [next assumption]` — Design the next experiment
- IF enough assumptions are validated after completed results: `$research-roadmap` — Check if research docs need updating based on learnings

### 8. Write Output

Present final plan to user. Ask:
- "Ready to write this experiment plan? Anything to adjust?"

Only after confirmation, write the output file.

## Output

### `research/experiments/[experiment-name].md` (or `research/{slug}/experiments/[experiment-name].md`)

```markdown
# Experiment: [Descriptive Name]

> Date designed: [current date]
> Status: Designed | Running | Completed
> Assumption: [from assumption-tracker, if applicable — include # reference]
> Priority: [from assumption-tracker score, if applicable]

## Hypothesis

**We believe that** [target segment]
**will** [expected behavior]
**because** [rationale from research]

**We'll know this is true when** [measurable outcome with specific threshold]

## Method

**Type**: [Landing page test / Fake-door / Concierge MVP / Survey / A/B test / Pricing test / Smoke test / Pre-sale / Wizard of Oz]
**Why this method**: [rationale — why this is the cheapest/fastest way to test this hypothesis]

### Setup
[Step-by-step instructions for setting up the experiment]

1. [Step 1]
2. [Step 2]
3. ...

### Tools Needed
- [Tool 1] — [purpose]
- [Tool 2] — [purpose]

### Audience
**Who**: [specific segment from ICP]
**How to reach them**: [channel — from GTM if available]
**Sample size**: [number needed for statistical significance]
**Recruitment method**: [how to get participants]

## Success Criteria

| Metric | Failure | Inconclusive | Success |
|--------|---------|--------------|---------|
| [Primary metric] | < [threshold] | [range] | ≥ [threshold] |
| [Secondary metric] | < [threshold] | [range] | ≥ [threshold] |

**Benchmarks**: [what industry/competitor data says is typical]

## Timeline

| Phase | Duration | Tasks |
|-------|----------|-------|
| Setup | [days] | [what to prepare] |
| Run | [days] | [data collection period] |
| Analyze | [days] | [how to analyze results] |
| **Total** | **[days]** | |

## Budget

| Item | Cost |
|------|------|
| [item] | [amount] |
| **Total** | **[amount]** |

## Decision Rules

### If Validated (success criteria met)
[Specific next actions — what to build, commit to, or double down on]

### If Invalidated (failure criteria met)
[Specific pivot — what to change, test next, or abandon]

### If Inconclusive
[What additional data is needed, whether to extend or redesign]

## Results

> Fill this section after the experiment completes.

**Status**: [Validated / Invalidated / Inconclusive]
**Date completed**: [date]

### Raw Data
[Key numbers and observations]

### Analysis
[What the data shows — connect back to hypothesis]

### Decision
[What was decided based on the results]

### Learnings
[What was learned beyond the hypothesis — surprises, side findings]

## Next Steps

**Recommended:** [recommended next step] — [one-line reason grounded in this artifact]

Other options:
- [conditional items from step 6 — only include items whose conditions are met]
```

Create the `research/experiments/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **One hypothesis per experiment.** If the user has multiple things to test, design separate experiments. Don't bundle.
- **Cheap and fast.** Every experiment should be completable in 1-4 weeks with minimal budget. If the design is expensive or slow, simplify.
- **Specific success criteria.** "Users like it" is not a success criterion. "≥40% of landing page visitors click 'Get Early Access'" is.
- **Present before writing.** Never write output files until the experiment design has been presented and validated.
- **Include decision rules.** Every experiment must specify what happens for each possible outcome. No experiment should end with "we'll figure it out."
- **Reference benchmarks.** Success thresholds should be grounded in industry benchmarks or competitor data, not arbitrary numbers.
- **Don't overdesign.** A simple survey can validate an assumption just as well as an elaborate A/B test. Recommend the simplest method that produces a clear signal.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/experiment-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
