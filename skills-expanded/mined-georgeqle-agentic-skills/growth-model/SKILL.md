---
name: growth-model
type: research
version: v0.8
description: Reforge-style growth loop design — acquisition, retention, and monetization loops
argument-hint: "[optional: specific loop type e.g. \"viral\", \"content\", \"paid\"]"
interview_depth: light
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Growth Model — Reforge-Style Growth Loop Design

Invoke as `$growth-model`.

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
- **Hard**: `research/gtm.md` (or `research/{slug}/gtm.md`) must exist. If not, tell the user to run `$gtm` first and stop.
- **Soft**: Read these if they exist:
  - `research/journey-map.md` — retention stages, aha moment, habit loop
  - `research/monetization.md` — pricing model, revenue mechanics
  - `research/hook-model.md` — engagement patterns, trigger-action-reward-investment cycle

## Process

### 0a. Product Path Manifest

Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope the growth model to the active product path by default. When modeling reveals that a deferred product path has significantly different growth characteristics, note the finding in a `## Product Path Implications` section.

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

- Read `research/metrics.md` (or `research/{slug}/metrics.md`) — success targets, KPIs, activation/engagement/retention/growth metrics
- Read `research/gtm.md` (or `research/{slug}/gtm.md`) — channels, acquisition strategy, pricing model, early traction tactics
- Read `research/journey-map.md` (or `research/{slug}/journey-map.md`) if it exists — customer journey stages, aha moment, habit loop, churn triggers
- Read `research/monetization.md` (or `research/{slug}/monetization.md`) if it exists — pricing tiers, upgrade triggers, revenue model
- Read `research/hook-model.md` (or `research/{slug}/hook-model.md`) if it exists — engagement loops, trigger-action-reward-investment cycle
- Read CLAUDE.md, README, and key source files for product context

### 2. Research Growth Loops

Use WebSearch with **4-6 targeted queries**:

1. **Reforge methodology** — "Reforge growth loops [category]"
2. **Domain-specific models** — "growth model [domain] examples"
3. **Competitor growth strategies** — "[competitor] growth strategy"
4. **Viral mechanisms** — "viral loop [product type]"
5. **Content loops** — "content loop B2B SaaS"
6. **Compounding mechanisms** — "compounding growth mechanisms [category]"

### 3. Identify Loop Candidates

Categorize potential loops from research and product context:

**Acquisition loops** — how new users are acquired:
- **Viral** — user invites user (referral, sharing, word-of-mouth)
- **Content** — content attracts user (SEO, UGC, community content)
- **Paid** — revenue funds acquisition (paid ads, sponsorships)
- **Sales** — revenue funds sales team (outbound, enterprise sales)

**Retention loops** — how users stay and deepen engagement:
- **Engagement** — usage deepens value (more data, personalization, history)
- **Network** — more users = more value (marketplace, social, collaboration)
- **Switching cost** — investment creates lock-in (integrations, customization, data)

**Monetization loops** — how revenue compounds:
- **Expansion** — usage drives upgrades (seat growth, tier upgrades, usage-based expansion)
- **Cross-sell** — one product leads to another (platform play, add-ons)

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Here are the growth loop candidates I see for this product. Which feel realistic given your current stage, resources, and product type? Any I should add or remove?"

### 4. Design Primary Loop

For the highest-potential loop, design it in detail:

- **Each step in the loop** — what happens at each stage, who does what
- **Conversion hypothesis between steps** — what must be true for users to move from one step to the next (each is a hypothesis until validated)
- **Compounding mechanism** — what makes the output feed back as input, creating exponential rather than linear growth
- **Key metric at each step** — the measurable signal that this step is working
- **Time-to-complete-cycle estimate** — how long one full loop iteration takes

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Is this primary loop realistic? What's the weakest step?"

### 5. Design Supporting Loops (1-2)

Design secondary loops that reinforce the primary:
- Show how they interact — which loop's output feeds another's input
- Identify where loops share steps or handoff points
- Keep these lighter than the primary — they support, not compete

### 6. Map Dependencies & Metrics

- Align each loop step with metrics from `research/metrics.md`
- Identify gaps where metrics don't cover loop steps
- Show loop-to-loop dependencies — where one loop's output feeds another's input
- Flag metrics that need to be added to track loop health

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Does this growth model align with your metrics framework? Any metric gaps or misalignments?"

### 7. Populate Next Steps

Before writing, check which files exist to populate the `## Next Steps` section contextually. Include a **Recommended** item (the single highest-impact next step given current project state) with a one-line reason, followed by **Other options** (2-4 alternatives). Use this format in the output:

## Next Steps

**Recommended:** `$experiment [top growth hypothesis]` — Test the highest-impact growth mechanism before committing to build

Other options:
- IF `specs/` exist and `tasks/roadmap.md` exists: `$roadmap` — Update roadmap with growth loop implementation work
- IF product is live or launching: `$experiment [growth hypothesis]` — Test the primary loop's weakest conversion hypothesis

**Impact-aware adjustments:**
- IF downstream impact is **Major**: prepend `$reconcile-research — [N] conflicts found in downstream docs` as the first item
- IF downstream impact is **Minor**: annotate relevant skill suggestions with "(stale — [brief description])"

### 8. Write Output

Only after the user confirms, write the output files.

### 9. Downstream Impact Check

After writing, check for downstream research documents that may be affected. Only check documents that exist on disk.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/metrics.md`
- `research/gtm.md`

For each existing downstream document:
1. Read it — focus on sections that reference growth strategy, acquisition channels, retention mechanisms, or expansion metrics
2. Identify **specific conflicts**: claims, assumptions, or references that contradict what was just decided. Examples:
   - A growth metric that doesn't align with the loop steps defined here
   - Channel strategy assumptions that don't match the acquisition loops designed
   - Retention targets that don't account for the retention loop mechanics
3. Note each conflict: downstream file, section, the stale claim (quote it), and what it should now say

**Classify the impact**:
- **None**: No downstream documents exist, or no conflicts found. Skip display entirely.
- **Minor** (1-2 small conflicts): Display conflicts to user inline.
- **Major** (3+ conflicts OR a foundational assumption changed — e.g., primary acquisition loop contradicts GTM channel strategy, retention model fundamentally differs from metrics targets): Display conflicts and strongly recommend `$reconcile-research`.

## Output

### `research/growth-model.md` (or `research/{slug}/growth-model.md`)

```markdown
# Growth Model

> Based on: research/metrics.md, research/gtm.md[, research/journey-map.md, research/monetization.md, research/hook-model.md]
> Date: [current date]
> Methodology: Reforge Growth Loops

## Summary
[2-3 sentences: the growth thesis — what loops drive this product's growth, why they compound, and what stage they're appropriate for]

## Loop Inventory

| Loop | Type | Potential | Stage-Readiness |
|------|------|-----------|-----------------|
| [loop name] | Acquisition / Retention / Monetization | High / Medium / Low | [why it fits or doesn't fit current stage] |

## Primary Growth Loop: [Loop Name]

**Type**: [Acquisition / Retention / Monetization]
**Compounding mechanism**: [what makes the output feed back as input]
**Cycle time estimate**: [how long one full loop iteration takes]

### Loop Steps

1. **[Step name]**
   - What happens: [description]
   - Key metric: [measurable signal]
   - Conversion hypothesis: [what must be true to reach step 2]

2. **[Step name]**
   - What happens: [description]
   - Key metric: [measurable signal]
   - Conversion hypothesis: [what must be true to reach step 3]

3. **[Step name]**
   - What happens: [description]
   - Key metric: [measurable signal]
   - Conversion hypothesis: [what must be true to feed back into step 1]

### Why This Loop Compounds
[Explain the specific mechanism — why does more output create more input? What's the flywheel effect?]

### Weakest Step
[Which conversion hypothesis is most uncertain, and what would validate it]

## Supporting Loop 1: [Loop Name]

**Type**: [Acquisition / Retention / Monetization]
**Compounding mechanism**: [what makes the output feed back as input]
**Cycle time estimate**: [how long one full loop iteration takes]

### Loop Steps
[Same structure as primary, lighter detail]

### Interaction with Primary Loop
[How this loop's output feeds the primary loop's input, or vice versa]

## Supporting Loop 2: [Loop Name]

**Type**: [Acquisition / Retention / Monetization]
**Compounding mechanism**: [what makes the output feed back as input]
**Cycle time estimate**: [how long one full loop iteration takes]

### Loop Steps
[Same structure as primary, lighter detail]

### Interaction with Primary Loop
[How this loop's output feeds the primary loop's input, or vice versa]

## Loop Interaction Map

[How loops feed each other — which loop's output becomes another's input]

- **[Loop A]** step [N] output --> feeds **[Loop B]** step [M] input
- **[Loop B]** step [N] output --> feeds **[Loop A]** step [M] input

## Metrics Alignment

| Loop Step | Metric | Current Target | Gap? |
|-----------|--------|---------------|------|
| [Primary loop - step 1] | [metric from metrics.md] | [target] | [Yes — no metric covers this / No] |
| [Primary loop - step 2] | [metric from metrics.md] | [target] | [Yes / No] |
| [Supporting loop - step 1] | [metric from metrics.md] | [target] | [Yes / No] |

### Metric Gaps
[List loop steps that have no corresponding metric in research/metrics.md — these need to be added]

## Growth Hypotheses to Test

| Hypothesis | Loop | Priority | Validation Method |
|-----------|------|----------|-------------------|
| [conversion hypothesis between loop steps] | [which loop] | High / Medium / Low | [how to test — experiment, survey, instrumentation] |

## Strategic Implications

### What This Model Means for Product
[Feature priorities that support loop mechanics — what to build to strengthen the weakest steps]

### What This Model Means for GTM
[How growth loops should shape channel investment, messaging, and launch sequencing]

### What This Model Means for Metrics
[Which metrics need to be added or reframed to track loop health]

### Stage-Appropriate Sequencing
[Which loops to activate now vs. later — match loop complexity to current stage]

<!-- Only include when downstream impact is Minor or Major -->
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

**Recommended:** `$experiment [top growth hypothesis]` — Test the highest-impact growth mechanism before committing to build

Other options:
- [conditional items from step 7 — only include items whose conditions are met]
```

### `research/growth-model-search-log.md` (or `research/{slug}/growth-model-search-log.md`)
Raw research log — queries, findings, evidence for each growth loop decision.

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stays in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Requires metrics + GTM.** Growth loops without success targets and channel strategy are theoretical.
- **Stage-appropriate.** Don't design viral loops for pre-launch products with no users. Match loop complexity to current stage.
- **Compounding is key.** If the loop's output doesn't feed back as input, it's not a loop — it's a funnel step.
- **Hypothesis-driven.** Every conversion between loop steps is a hypothesis until validated.
- **Present before writing.** Never write output files until the growth model has been presented and validated.
- **Do not overwrite existing `research/growth-model.md`** (or `research/{slug}/growth-model.md`) without asking the user first.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/growth-model-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
