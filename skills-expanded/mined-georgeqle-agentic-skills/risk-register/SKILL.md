---
name: risk-register
description: Broad risk assessment — key-person, technical, regulatory, competitive, financial, and execution risks beyond product/market
type: analysis
version: v0.3
argument-hint: "[optional: focus area e.g. \"technical\", \"regulatory\", \"financial\"]"
interview_depth: light
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Risk Register — Systematic Risk Assessment

Invoke as `$risk-register`.

Identifies and tracks risks beyond product/market: key-person, technical, regulatory, competitive, financial, and execution risks. Complements `$assumption-tracker` (which focuses on product/market assumptions) with broader organizational and environmental risks.

## Soft Prerequisites

- Read all that exist: `research/icp.md`, `research/competitive-analysis.md`, `research/gtm.md`, `research/monetization.md`, `research/runway-model.md`, `research/assumption-tracker.md`, CLAUDE.md, README
- The more context exists, the more thorough the risk identification.

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

Read all available research docs and codebase files. Extract signals relevant to risk:
- **Financial**: runway, burn rate, revenue concentration
- **Technical**: tech debt, single points of failure, scaling concerns
- **Market**: competitive threats, market shifts, regulatory changes
- **Team**: key-person dependencies, skill gaps, hiring needs
- **Execution**: timeline risks, scope creep, dependency chains

### 2. Identify Risks

Use WebSearch with **3-5 targeted queries** for domain-specific risks:
1. "[industry/category] startup risks"
2. "[category] regulatory requirements"
3. "[technology stack] scaling risks"
4. "[category] common failure modes"

Systematically identify risks in each category:

#### A. Key-Person Risk
- Single points of failure in the team
- Critical knowledge held by one person
- Founder dependency

#### B. Technical Risk
- Architecture limitations, scaling bottlenecks
- Security vulnerabilities, data privacy
- Dependency on third-party services
- Technical debt accumulation

#### C. Regulatory & Legal Risk
- Compliance requirements (GDPR, SOC2, industry-specific)
- IP risks, patent exposure
- Terms of service dependencies on platforms

#### D. Competitive Risk
- Well-funded competitor entering the space
- Platform risk (building on someone else's platform)
- Open-source alternatives emerging

#### E. Financial Risk
- Revenue concentration (one big customer)
- Runway constraints
- Pricing pressure from competitors
- Cost structure changes (API pricing, infrastructure)

#### F. Execution Risk
- Scope creep, feature bloat
- Hiring challenges
- Timeline slippage
- Integration complexity

### 3. Score Each Risk

| Dimension | Scale |
|-----------|-------|
| **Likelihood** | 1 (unlikely) → 5 (near certain) |
| **Impact** | 1 (minor setback) → 5 (existential threat) |
| **Priority** | Likelihood × Impact (max 25) |

### 4. Define Mitigations

For each high-priority risk (score ≥ 12):
- **Accept**: Acknowledge and monitor
- **Mitigate**: Actions to reduce likelihood or impact
- **Transfer**: Insurance, contracts, or partnerships
- **Avoid**: Change plans to eliminate the risk

### 5. Present & Validate

Present the top risks to the user. If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Here are the highest-priority risks I've identified. Any I'm missing or scoring wrong?"
- "Are there any risks you're already mitigating that I should note?"

Incorporate feedback before proceeding.

### 6. Write Output

Only after confirmation, write the output file.

## Output

### `research/risk-register.md` (or `research/{slug}/risk-register.md`)

```markdown
# Risk Register

> Last updated: [current date]
> Sources: [research docs reviewed]
> Total risks: [count] | High priority: [count]

## Summary
[2-3 sentences: the top risks and overall risk posture]

## Top Risks

| # | Risk | Category | Likelihood | Impact | Priority | Mitigation |
|---|------|----------|-----------|--------|----------|------------|
| 1 | [risk] | [category] | [1-5] | [1-5] | [L×I] | [strategy] |
| ... | | | | | | |

## Key-Person Risks
| Risk | Likelihood | Impact | Priority | Mitigation |
|------|-----------|--------|----------|------------|
| [risk] | [1-5] | [1-5] | [L×I] | [action] |

## Technical Risks
[Same table format]

## Regulatory & Legal Risks
[Same table format]

## Competitive Risks
[Same table format]

## Financial Risks
[Same table format]

## Execution Risks
[Same table format]

## Mitigation Plan

### Immediate Actions (This Month)
1. [Action] — mitigates [risk #]
2. ...

### Ongoing Monitoring
| Risk | Trigger Signal | Check Frequency |
|------|---------------|-----------------|
| [risk] | [what to watch for] | [weekly/monthly/quarterly] |

## Next Steps

**Recommended:** [recommended skill] — [one-line reason grounded in the highest-priority risk]

Other options:
- `$assumption-tracker` — Cross-reference product/market assumptions with these broader risks
- `$experiment [top risk assumption]` — Test the riskiest uncertainty when it can be validated cheaply
- `$reconcile-research` — Update downstream research if risk findings contradict existing assumptions
- `$research-roadmap` — Check overall project status
```

Create the `research/` directory if it doesn't exist.

### 7. Populate Next Steps

Before writing, choose one recommended next step using the first applicable rule:

1. IF a high-priority risk is a product/market assumption: recommend `$assumption-tracker`.
2. IF the top risk can be cheaply validated: recommend `$experiment [top risk assumption]`.
3. IF the findings contradict existing research: recommend `$reconcile-research`.
4. Otherwise recommend `$research-roadmap`.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Complement, don't duplicate.** Product/market assumptions belong in `$assumption-tracker`. Cover organizational, technical, regulatory, competitive, financial, and execution risks.
- **Be specific.** "Competition" is not a risk. "Well-funded competitor X launching a free tier in Q3" is.
- **Present before writing.** Never write until the user validates the assessment.
- **Score honestly.** Don't inflate risks to seem thorough. Low-probability risks should be scored low.
- **Update, don't duplicate.** If `research/risk-register.md` exists, ask whether to update or overwrite.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/risk-register-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
