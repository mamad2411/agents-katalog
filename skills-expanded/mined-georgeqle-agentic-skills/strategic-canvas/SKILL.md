---
name: strategic-canvas
description: Blue Ocean strategic canvas — extract competing factors, build value curves, apply Four Actions Framework (eliminate/reduce/raise/create)
type: research
version: v0.9
invocation: sub-skill
parent: positioning
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Strategic Canvas — Blue Ocean Value Curve Analysis

## Parent Orchestrator Routing

Run only through the parent orchestrator `$positioning` as part of its Research Session Loop. If the user needs to continue pending framework work, tell them to start a fresh Codex session and re-invoke `$positioning` with the same product/research path argument when present, for example `$positioning research/afps-tracker`.

Do not ask users to invoke this framework directly or with a path-shaped child framework command. Do not emit downstream routing labels or command recommendations from this framework subskill; parent synthesis owns downstream routing after canonical artifacts are approved.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include downstream routing language. The approval request itself is the next action. Parent synthesis owns downstream routing after approved artifacts are written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Purpose

Applies the Blue Ocean Strategy framework (Kim & Mauborgne) to identify positioning opportunities by mapping industry competing factors, plotting value curves for current competitors, and applying the Four Actions Framework to find uncontested market space. Produces an intermediate artifact for the parent `$positioning` synthesis.

## Prerequisites

- **Hard**: `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) must exist. If not, tell the user to run `$competitive-analysis` first and stop.
- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `$customer-discovery` first and stop.
- **Soft**: Read if they exist:
  - `research/journey-map.md` — where overserved/underserved moments appear
  - `research/customer-feedback.md` — what customers value and what they ignore
  - `research/positioning.md` — existing positioning context

## Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

## Process

### 1. Load Context

- Read `research/competitive-analysis.md` — competitor landscape, features, strengths, weaknesses
- Read `research/icp.md` — what customers actually value vs. what industry assumes they value
- Read soft prerequisites if available

### 2. Extract Competing Factors

Identify 8-12 factors the industry competes on. These are the dimensions buyers evaluate:

- Use WebSearch with 3-5 queries: "[category] comparison criteria", "[category] buyer evaluation", "[competitor] vs [competitor] comparison"
- Sources: review sites, comparison pages, buyer guides, analyst reports
- Include both explicit (features, price) and implicit (brand trust, ease of switching) factors

Present factors to user. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "These are the competing factors I found for this industry. Which are missing, irrelevant, or mis-weighted?"

### 3. Build Value Curves

For each major competitor (3-5) plus the user's product, score each competing factor on a relative scale (Low / Medium / High):

| Factor | Competitor A | Competitor B | Competitor C | This Product |
|--------|-------------|-------------|-------------|--------------|
| [factor] | [L/M/H] | [L/M/H] | [L/M/H] | [L/M/H] |

Identify patterns:
- **Convergence zones** — where all competitors score similarly (commoditized factors)
- **Divergence zones** — where one player stands out
- **Overserved factors** — high investment, low customer value
- **Underserved factors** — low investment, high customer need

### 4. Apply Four Actions Framework

For each competing factor, determine the strategic action:

**Eliminate** — Which factors that the industry takes for granted should be eliminated?
- Factors that add cost but not customer value
- Features customers never use or don't care about
- "Me too" capabilities that don't differentiate

**Reduce** — Which factors should be reduced well below the industry standard?
- Overengineered features customers don't need at that level
- Factors where "good enough" beats "best in class"

**Raise** — Which factors should be raised well above the industry standard?
- Factors where current solutions frustrate customers
- Dimensions where improvement creates outsized value

**Create** — Which factors should be created that the industry has never offered?
- New value dimensions competitors haven't considered
- Needs revealed by journey-map or customer feedback
- Adjacent problems no one in the category addresses

Validate with user. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "Here are the Four Actions. Which eliminate/reduce actions feel too aggressive? Which raise/create actions lack evidence?"

### 5. Define Target Value Curve

Plot the desired value curve for the product — the strategic profile that creates uncontested space:

- Show clear differentiation from competitor curves
- Validate that eliminate/reduce actions genuinely reduce cost or complexity
- Validate that raise/create actions genuinely increase customer value
- Identify the "divergent" shape that signals a blue ocean move

### 6. Write Output

Only after user approval.

## Output

### `research/positioning-strategic-canvas.md` (or `research/{slug}/positioning-strategic-canvas.md`)

```markdown
# Strategic Canvas — Blue Ocean Analysis

> Based on: research/competitive-analysis.md, research/icp.md
> Date: [current date]
> Methodology: Blue Ocean Strategy (Kim & Mauborgne)

## Industry Competing Factors

| # | Factor | Industry Importance | Customer Importance | Gap |
|---|--------|-------------------|--------------------|----|
| 1 | [factor] | [H/M/L] | [H/M/L] | [over/under/aligned] |

## Value Curves

| Factor | [Comp A] | [Comp B] | [Comp C] | This Product (Current) | This Product (Target) |
|--------|----------|----------|----------|----------------------|---------------------|
| [factor] | [1-5] | [1-5] | [1-5] | [1-5] | [1-5] |

### Convergence Zones (Commoditized)
- [factors where all competitors cluster]

### Divergence Opportunities
- [factors where the product can break away]

## Four Actions Framework

### Eliminate
| Factor | Why Eliminate | Cost Saved | Risk |
|--------|-------------|-----------|------|
| [factor] | [rationale] | [impact] | [what could go wrong] |

### Reduce
| Factor | Current Level | Target Level | Rationale |
|--------|--------------|-------------|-----------|
| [factor] | [current] | [target] | [why good enough works] |

### Raise
| Factor | Current Level | Target Level | Evidence of Demand |
|--------|--------------|-------------|-------------------|
| [factor] | [current] | [target] | [source] |

### Create
| Factor | Description | Customer Need | Evidence |
|--------|-------------|---------------|----------|
| [factor] | [what it is] | [what need it serves] | [source] |

## Target Strategic Profile

**Blue ocean thesis**: [one sentence — what uncontested space this creates]
**Key trade-off**: [what you give up to get there]
**Evidence strength**: [Strong / Moderate / Weak — with justification]

## Implications for Positioning Synthesis

[How this canvas analysis should influence the final positioning — what it suggests for market category, differentiation strategy, and messaging emphasis]
```

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable work goes in `tasks/todo.md`.
- Human-only external actions go in `tasks/manual-todo.md` with blocking/dependency annotations.
- Condition-gated records go in `tasks/record-todo.md`.
- Cadence-based reviews go in `tasks/recurring-todo.md`.

## Constraints

- **Intermediate artifact only.** This produces `research/positioning-strategic-canvas.md`, not the canonical `research/positioning.md`.
- **Evidence-grounded scoring.** Value curve scores must cite competitive analysis or research — no guessing.
- **Honest about gaps.** If the product has no clear blue ocean move, say so. Not every product needs category creation.
- **Present before writing.** Never write output files until findings are validated.
- **Four Actions must be actionable.** Each action should connect to a concrete product or positioning decision.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/strategic-canvas-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
