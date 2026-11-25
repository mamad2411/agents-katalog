---
name: value-prop-canvas
description: Strategyzer-style jobs/pains/gains to features/relievers/creators fit validation
type: research
version: v0.9
argument-hint: "[optional: specific job or segment to focus on]"
interview_depth: light
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell, instead of the target skill. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Value Proposition Canvas — Solution-Customer Fit Validation

Invoke as `$value-prop-canvas`.

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

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `$customer-discovery` first and stop.
- **Soft**: Read these if they exist:
  - `research/competitive-analysis.md` — competitor landscape and alternative solutions
  - `research/journey-map.md` — where jobs, pains, gains, and aha moments occur in the user/customer lifecycle
  - `research/positioning.md` — market framing to avoid contradicting accepted positioning
  - `research/idea-brief.md` — product concept and hypothesis

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

- Read `research/icp.md` — ICP segments, jobs, pains, gains, trigger events
- Read `research/competitive-analysis.md` if it exists — competitor landscape, alternative solutions
- Read `research/idea-brief.md` if it exists — product concept and hypothesis
- Read CLAUDE.md, README, and key source files for product context

### 2. Research VPC Methodology

Use WebSearch with **4-6 targeted queries**:

1. **Domain VPC** — "value proposition canvas [domain]"
2. **JTBD mapping** — "jobs to be done [category]"
3. **Strategyzer methodology** — "Strategyzer value proposition design [industry]"
4. **Customer profile patterns** — "customer jobs pains gains [category]"
5. **Value map examples** — "value map pain relievers gain creators examples"

### 3. Build Customer Profile

For the primary ICP segment, construct the Customer Profile:

**Jobs** (functional, social, emotional):
- Functional jobs — tasks they're trying to complete
- Social jobs — how they want to be perceived
- Emotional jobs — feelings they seek or avoid

Rank each job by importance (critical / important / nice-to-have).

**Pains**:
- Undesired outcomes, obstacles, risks
- Rank by severity: extreme / high / moderate

**Gains**:
- Outcomes and benefits they want
- Rank by relevance: required / expected / desired / unexpected

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Here's the Customer Profile I've built from ICP research. Which jobs, pains, or gains are missing, overstated, or mis-ranked?"

### 4. Build Value Map

Map the product's features and services to pain relievers and gain creators:

**Products & Services** — what the product offers (features, capabilities, services)

**Pain Relievers** — for each: which specific pain does it relieve? How completely?

**Gain Creators** — for each: which specific gain does it create? How significantly?

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Does this Value Map accurately reflect what the product does? Any features missing or claims overstated?"

### 5. Score Fit

For each customer job, evaluate how well the Value Map addresses it:

| Job | Fit Score | Evidence | Risk |
|-----|-----------|----------|------|
| [job] | Strong Fit / Partial Fit / No Fit / Gap | [what supports this score] | [if No Fit or Gap, what's at stake] |

Flag all jobs with **No Fit** or **Gap** as risks requiring attention.

If the session is already in Plan mode and there are 2-3 concrete choices, prefer `request_user_input`; otherwise ask in plain text:
- "Do these fit scores reflect reality? Are there fits I'm overrating or gaps I'm missing?"

### 6. Identify Gaps & Risks

Summarize findings across four dimensions:

1. **Unaddressed jobs** — customer jobs with no corresponding product capability
2. **Partially addressed pains** — pain relievers that don't fully resolve the pain
3. **Missing gain creators** — desired gains with no corresponding product feature
4. **Over-investment areas** — features that don't map to important jobs (wasted effort)

Prioritize by ICP segment importance — gaps in critical jobs matter more than gaps in nice-to-have jobs.

### 7. Populate Next Steps

Include a **Recommended** item (the single highest-impact next step given current project state) with a one-line reason, followed by **Other options** (2-4 alternatives). Use this format in the output:

## Next Steps

**Recommended:** `$positioning` — return to the default AFPS route by framing validated fit in the market

Other options:
- IF gaps identified: `$positioning` — Define product positioning from gap evidence (if `research/positioning.md` missing), or `$user-flow-map [top gap]` — Map flow structure for the highest-priority gap before UI requirements and layout variants
- IF no `research/competitive-analysis.md`: `$competitive-analysis` — Understand how alternatives address the same jobs
- IF `research/positioning.md` exists: `$user-flow-map [validated fit direction]` — return to the prototype path by mapping flow structure before UI requirements and layout variants
- IF business model, revenue, channel, cost, or defensibility risk remains material: `$lean-canvas` — optional synthesis now that fit is validated

### 8. Write Output

Only after the user confirms, write the output files.

### 9. Downstream Impact Check

After writing, check for downstream research documents that may be affected.

**Downstream documents to check** (use `{slug}/` prefix when product-path scope is active):
- `research/positioning.md`
- `research/lean-canvas.md`

For each existing downstream document:
1. Read it — focus on sections referencing customer jobs, pains, gains, or solution fit
2. Identify conflicts where claims don't align with the new VPC findings
3. Note each conflict: file, section, stale claim, what it should now say

**Classify the impact**:
- **None**: No downstream docs exist, or no conflicts. Skip display.
- **Minor** (1-2 small conflicts): Display inline.
- **Major** (3+ conflicts OR fit scores changed significantly, new gaps identified, customer profile substantially revised): Display and recommend `$reconcile-research`.

## Output

### `research/value-prop.md` (or `research/{slug}/value-prop.md`)

```markdown
# Value Proposition Canvas

> Based on: research/icp.md[, research/competitive-analysis.md, research/idea-brief.md]
> Date: [current date]
> Methodology: Strategyzer Value Proposition Canvas

## Summary
[2-3 sentences: the fit thesis — how well the product addresses the customer's most important jobs, where fit is strongest, and where the critical gaps are]

## Customer Profile

### Jobs

| # | Job | Type | Importance | Description |
|---|-----|------|------------|-------------|
| J1 | [job name] | Functional / Social / Emotional | Critical / Important / Nice-to-have | [what they're trying to accomplish] |

### Pains

| # | Pain | Severity | Related Jobs | Description |
|---|------|----------|--------------|-------------|
| P1 | [pain name] | Extreme / High / Moderate | J1, J2 | [undesired outcome, obstacle, or risk] |

### Gains

| # | Gain | Relevance | Related Jobs | Description |
|---|------|-----------|--------------|-------------|
| G1 | [gain name] | Required / Expected / Desired / Unexpected | J1, J3 | [outcome or benefit they want] |

## Value Map

### Products & Services
- [Feature/capability 1] — [what it does]
- [Feature/capability 2] — [what it does]

### Pain Relievers

| Pain Reliever | Addresses Pain | Completeness | How It Relieves |
|---------------|---------------|--------------|-----------------|
| [feature/capability] | P1 | Full / Partial / Minimal | [mechanism of relief] |

### Gain Creators

| Gain Creator | Addresses Gain | Significance | How It Creates |
|--------------|---------------|--------------|----------------|
| [feature/capability] | G1 | High / Medium / Low | [mechanism of creation] |

## Fit Scorecard

| Job | Fit Score | Evidence | Risk |
|-----|-----------|----------|------|
| J1: [job name] | Strong Fit / Partial Fit / No Fit / Gap | [what supports this assessment] | [risk if unaddressed] |

**Overall Fit**: [Strong / Moderate / Weak] — [one-sentence justification]

## Gap Analysis

### Unaddressed Jobs
- [Job] — [why it's unaddressed, impact on customer segment]

### Partially Addressed Pains
- [Pain] — [what's addressed, what's missing]

### Missing Gain Creators
- [Gain] — [no product capability maps to this gain]

### Over-Investment Areas
- [Feature] — [maps to no important job; potential wasted effort]

## Strategic Implications
[What this fit analysis means for product strategy — what to double down on, what to build, what to deprioritize]

<!-- Only include when downstream impact is Minor or Major -->
## Downstream Impact

> Checked: [list of downstream docs checked]
> Impact: Minor | Major

### Conflicts Found

1. **research/[file].md** — [Section Name]
   - **Stale**: "[exact quote]"
   - **Now**: [what VPC findings say instead]

[For Major only:]
> **Recommended action**: Run `$reconcile-research` to audit and fix all affected downstream documents.

## Next Steps

**Recommended:** `$positioning` — solution-customer fit validated; positioning determines how to frame this value in the market

Other options:
- [conditional items from step 7]
```

### `research/value-prop-search-log.md` (or `research/{slug}/value-prop-search-log.md`)
Raw research log — queries, findings, evidence for each VPC decision.

Create the `research/` directory if it doesn't exist.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- **Requires ICP.** VPC without knowing the customer is guesswork.
- **Customer-grounded.** Every job, pain, and gain must trace to ICP research or customer evidence, not assumptions.
- **Be honest about fit.** If fit is weak, say so — that's a critical finding, not a failure.
- **Present before writing.** Never write output files until the canvas has been presented and validated.
- **VPC ≠ positioning.** Validate solution-customer fit; positioning determines market framing. They are distinct steps.
- **Do not overwrite existing `research/value-prop.md`** without asking the user first.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/value-prop-canvas-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
