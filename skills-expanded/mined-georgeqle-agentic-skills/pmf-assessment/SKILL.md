---
name: pmf-assessment
type: research
version: v0.9
description: Sean Ellis PMF survey design + qualitative signal analysis for post-launch fit measurement
argument-hint: "[optional: specific signal or segment to focus on]"
interview_depth: light
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# PMF Assessment — Product-Market Fit Measurement

Invoke as `$pmf-assessment`.

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

- **Hard**: `research/metrics.md` (or `research/{slug}/metrics.md`) must exist. If not, tell the user to run `$metrics` first and stop.
- **Soft**: Read these if they exist:
  - `research/icp.md` — target customer segments, pain points, jobs-to-be-done
  - `research/journey-map.md` — critical moments, aha moment, drop-off points
  - `research/customer-feedback.md` — real user language, complaints, praise, churn signals

## Process

### 0a. Product Path Manifest

Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope the PMF assessment to the active product path by default. When PMF signals suggest a deferred product path has stronger product-market fit than the active path, add a `## Product Path Implications` section recommending `$product-line activate`.

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

- Read `research/metrics.md` — success targets, north star metric, current performance data
- Read `research/icp.md` if it exists — target segments, pain points, jobs-to-be-done
- Read `research/journey-map.md` if it exists — critical moments, aha moment, engagement patterns
- Read `research/customer-feedback.md` if it exists — real user language, sentiment, churn signals
- Read CLAUDE.md, README, and key source files for product context

### 2. Launch Check

Detect whether the product has live users. Look for evidence:
- `research/customer-feedback.md` exists with real user quotes
- Analytics references in metrics or other research docs
- Deployed URLs in README or CLAUDE.md
- User counts, revenue figures, or usage data in any research file

**If no evidence of live product:**

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "I don't see evidence of a live product with real users. PMF assessment requires actual user data. Would you like to design the survey framework now for future use, or should we focus on `$spec-interview` or `$roadmap` to get to launch first?"

If the user wants to proceed anyway, continue but mark all outputs as "pre-launch framework — requires live data to score."

### 3. Research Sean Ellis Methodology

Use WebSearch with **4-6 targeted queries**:

1. **Core methodology** — "Sean Ellis PMF survey methodology", "very disappointed question PMF"
2. **Domain-specific signals** — "product market fit signals [category]", "PMF measurement [domain]"
3. **Advanced frameworks** — "superhuman PMF engine", "Rahul Vohra PMF framework"
4. **Qualitative indicators** — "qualitative PMF indicators", "product market fit signs [industry]"
5. **Threshold context** — "40% very disappointed threshold context", "PMF score benchmarks [category]"

### 4. Design PMF Survey

**Core question**: "How would you feel if you could no longer use [product]?"
- Very disappointed
- Somewhat disappointed
- Not disappointed
- N/A — I no longer use [product]

**Follow-up questions by response:**

For "Very disappointed" respondents:
- What is the main benefit you get from [product]?
- What would you likely use as an alternative?
- How would you describe [product] to a friend?

For "Somewhat disappointed" respondents:
- What would you likely use instead?
- What could we improve to make [product] indispensable?

For "Not disappointed" respondents:
- Why not? What's missing for you?
- What were you hoping [product] would do that it doesn't?

**Product-specific follow-ups** (3-5 additional questions based on product context):
- Tailored to ICP jobs-to-be-done and journey critical moments
- Focused on understanding *why* users feel the way they do, not just *that* they do

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Here's the PMF survey design. Are the follow-up questions tailored enough to your product? Any segments you want surveyed separately?"

### 5. Qualitative Signal Analysis

**If `research/customer-feedback.md` exists**, analyze for PMF signals:

| Signal Category | What to Look For | PMF Indicator |
|----------------|-------------------|---------------|
| Organic word-of-mouth | Unprompted referrals, social mentions, "told my friend about" | Strong positive |
| Usage frequency | Daily/weekly active patterns, session depth | Engagement strength |
| Emotional language | "love", "can't live without", "game-changer" vs. "it's fine", "okay" | Sentiment intensity |
| Feature requests vs. complaints | Ratio of "add X" to "fix Y" — wanting more vs. wanting less broken | Product maturity |
| Churn reasons | Why people leave — alternatives, missing features, price, no need | Fit gaps |
| Expansion signals | Upgrades, team invites, increased usage, API adoption | Growth readiness |

**If no feedback file exists**, design the signal checklist for future analysis and note which signals to start tracking immediately.

### 6. Scoring Framework

**Quantitative threshold** (Sean Ellis):
- **Strong PMF**: >40% "very disappointed" responses
- **Moderate PMF**: 25-40% "very disappointed" responses
- **Weak PMF**: <25% "very disappointed" responses

**Qualitative signals checklist**:
1. Organic word-of-mouth happening without prompting
2. Usage frequency increasing or stable (not declining)
3. Emotional language in feedback (strong positive sentiment)
4. Feature requests outnumber complaints
5. Low voluntary churn / high retention
6. Expansion behavior (upgrades, invites, deeper usage)

**Combined scoring**:
- **Strong PMF**: >40% "very disappointed" AND 3+ qualitative signals present
- **Moderate PMF**: 25-40% "very disappointed" OR 2 qualitative signals present
- **Weak PMF**: <25% "very disappointed" AND fewer than 2 qualitative signals

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Does this scoring framework match your context? Any signals more/less important for your market?"

### 7. Populate Next Steps

Include a **Recommended** item (the single highest-impact next step given current project state) with a one-line reason, followed by **Other options** (2-4 alternatives), conditional on PMF strength. Use this format in the output:

**Weak PMF:**

## Next Steps

**Recommended:** `$customer-feedback [top user complaint]` — deep-dive on the weakest area to understand what's broken

Other options:
- `$customer-discovery` — Re-examine customer fit; you may be selling to the wrong segment
- `$journey-map` — Map where users drop off to find the biggest gap

**Moderate PMF:**

## Next Steps

**Recommended:** `$growth-model` — model growth levers to strengthen engagement before scaling

Other options:
- `$hook-model` — Design habit loops around what's already working
- `$customer-feedback [most-requested feature]` — Deep-dive on what "somewhat disappointed" users want more of

**Strong PMF:**

## Next Steps

**Recommended:** `$growth-model` — model growth channels to scale what's working

Other options:
- `$roadmap` — Plan the scaling phase with confidence
- `$gtm` — Build go-to-market plan grounded in proven fit

### 8. Write Output

Only after the user confirms, write the output files.

### 9. Downstream Impact Check

After writing, check for downstream research documents that may be affected.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/metrics.md`
- `research/growth-model.md`

For each existing downstream document:
1. Read it — focus on PMF-related sections, success thresholds, growth assumptions
2. Identify conflicts where assumptions don't align with the PMF assessment findings
3. Note each conflict: file, section, stale claim, what it should now say

**Classify the impact**:
- **None**: No downstream docs exist, or no conflicts. Skip display.
- **Minor** (1-2 small conflicts): Display inline.
- **Major** (3+ conflicts OR PMF level changes growth assumptions, success targets need revision, segment focus shifted): Display and recommend `$reconcile-research`.

## Output

### `research/pmf-assessment.md` (or `research/{slug}/pmf-assessment.md`)

```markdown
# PMF Assessment

> Based on: research/metrics.md[, research/icp.md, research/journey-map.md, research/customer-feedback.md]
> Date: [current date]
> Methodology: Sean Ellis PMF Survey + Qualitative Signal Analysis
> Launch Status: Live with users | Pre-launch framework

## Summary
[2-3 sentences: the PMF thesis — current fit level, key evidence, primary recommendation]

## Launch Status Assessment

**Status**: [Live with N users / Pre-launch / Early access]
**Evidence**: [what signals indicate launch status]
**Data availability**: [what data exists vs. what's needed for full scoring]

## PMF Survey Design

### Core Question

"How would you feel if you could no longer use [product]?"

| Response | Purpose |
|----------|---------|
| Very disappointed | PMF signal — these are your core users |
| Somewhat disappointed | Potential — understand what's missing |
| Not disappointed | Fit gap — understand why not |
| N/A — no longer use | Churn signal — understand what happened |

### Follow-Up Questions

#### For "Very Disappointed" Respondents
1. [Question] — *Rationale: [why this question matters for this product]*
2. [Question] — *Rationale: [why]*
3. [Question] — *Rationale: [why]*

#### For "Somewhat Disappointed" Respondents
1. [Question] — *Rationale: [why]*
2. [Question] — *Rationale: [why]*

#### For "Not Disappointed" Respondents
1. [Question] — *Rationale: [why]*
2. [Question] — *Rationale: [why]*

#### Product-Specific Follow-Ups (All Respondents)
1. [Question] — *Rationale: [why]*
2. [Question] — *Rationale: [why]*

### Recommended Sample Size
- **Minimum viable**: 40 responses (for directional signal)
- **Statistically meaningful**: 100+ responses
- **Ideal**: 200+ responses with segment breakdown

### Segment Breakdown

Survey these segments separately for segment-level PMF signals:

| Segment | Why Separate | Expected Difference |
|---------|-------------|-------------------|
| [segment] | [reason] | [hypothesis] |

## Qualitative Signal Analysis

| Signal | Current Evidence | Status |
|--------|-----------------|--------|
| Organic word-of-mouth | [evidence or "awaiting data"] | Present / Absent / Awaiting data |
| Usage frequency patterns | [evidence or "awaiting data"] | Present / Absent / Awaiting data |
| Emotional language | [evidence or "awaiting data"] | Present / Absent / Awaiting data |
| Feature requests vs. complaints | [evidence or "awaiting data"] | Present / Absent / Awaiting data |
| Churn reasons | [evidence or "awaiting data"] | Present / Absent / Awaiting data |
| Expansion signals | [evidence or "awaiting data"] | Present / Absent / Awaiting data |

**Qualitative signals present**: [count] / 6

## PMF Scoring Framework

### Quantitative Threshold (Sean Ellis)

| Level | "Very Disappointed" % | Interpretation |
|-------|----------------------|----------------|
| Strong | >40% | Clear product-market fit — scale with confidence |
| Moderate | 25-40% | Promising but not locked in — improve before scaling |
| Weak | <25% | Fit not established — iterate on product or segment |

### Signal Weights

[Note any domain-specific factors that shift the threshold. The 40% number is a guideline, not gospel — context matters.]

### Combined Assessment

| PMF Level | Quantitative | Qualitative (3+ of 6) | Action Mode |
|-----------|-------------|----------------------|-------------|
| Strong PMF | >40% | AND 3+ signals | Scale |
| Moderate PMF | 25-40% | OR 2 signals | Strengthen |
| Weak PMF | <25% | AND <2 signals | Iterate |

## Current PMF Estimate

[If data available:]
**Quantitative score**: [X]% "very disappointed" — [Strong/Moderate/Weak]
**Qualitative signals**: [N]/6 present
**Combined assessment**: [Strong/Moderate/Weak] PMF
**Confidence**: [High/Medium/Low] — based on [sample size, data quality, recency]

[If pre-launch:]
> **Pre-launch framework** — no PMF score can be calculated without live user data. Use this framework once you have 40+ active users to survey. Focus areas before measuring: [specific recommendations].

## Recommended Actions by PMF Level

| PMF Level | Primary Action | Secondary Action | Avoid |
|-----------|---------------|-----------------|-------|
| Weak | Iterate on core value prop or re-examine segment fit | Interview churned users, test with adjacent segment | Scaling spend, feature bloat |
| Moderate | Double down on what "very disappointed" users love | Improve for "somewhat disappointed" segment | Premature scaling, pivoting away from what works |
| Strong | Scale acquisition channels | Expand to adjacent segments | Over-iterating on core (it works), ignoring ops scaling |

## Strategic Implications

### What This Means for Product
[How PMF level should influence product decisions]

### What This Means for Growth
[How PMF level should influence growth investment]

### What This Means for Fundraising
[How PMF level affects investor conversations and timing]

<!-- Only include when downstream impact is Minor or Major -->
## Downstream Impact

> Checked: [list of downstream docs checked]
> Impact: Minor | Major

### Conflicts Found

1. **research/[file].md** — [Section Name]
   - **Stale**: "[exact quote]"
   - **Now**: [what PMF assessment says instead]

[For Major only:]
> **Recommended action**: Run `$reconcile-research` to audit and fix all affected downstream documents.

## Next Steps

[Use the PMF-level-conditional format from step 7]
```

### `research/pmf-assessment-search-log.md` (or `research/{slug}/pmf-assessment-search-log.md`)
Raw research log — queries, findings, evidence for each PMF assessment decision.

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Requires metrics.** PMF measurement without success targets is directionless. If `research/metrics.md` doesn't exist, stop and run `$metrics` first.
- **Honest about data availability.** If no live users, say so clearly — do not fabricate PMF scores.
- **The 40% threshold is a guideline, not gospel.** Context matters — note when domain-specific factors change the threshold (e.g., enterprise B2B with few customers, two-sided marketplaces, regulated industries).
- **Present before writing.** Never write output files until the assessment has been presented and validated.
- **Do not overwrite existing `research/pmf-assessment.md`** without asking the user first.
- **PMF is a spectrum, not binary.** Frame results as a continuum with actionable next steps at each level. Avoid "you have PMF" / "you don't have PMF" absolutes.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/pmf-assessment-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
