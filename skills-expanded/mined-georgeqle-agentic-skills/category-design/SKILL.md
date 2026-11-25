---
name: category-design
description: Play Bigger category creation — category diagnosis, naming, POV development, ecosystem mapping
type: research
version: v0.9
invocation: sub-skill
parent: positioning
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Category Design — Play Bigger Category Creation

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

Applies the Play Bigger category design framework to determine whether the product should compete in an existing category, carve a subcategory, or create an entirely new category. When category creation is warranted, develops category naming, Point of View (POV), and ecosystem mapping. Produces an intermediate artifact for the parent `$positioning` synthesis.

## Prerequisites

- **Hard**: `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) must exist. If not, tell the user to run `$competitive-analysis` first and stop.
- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `$customer-discovery` first and stop.
- **Hard**: `research/journey-map.md` (or `research/{slug}/journey-map.md`) must exist. If not, tell the user to run `$journey-map` first and stop.
- **Soft**: Read if they exist:
  - `research/customer-feedback.md` — language that signals category dissatisfaction
  - `research/positioning-jtbd.md` — job framing that may define a new category boundary
  - `research/positioning-strategic-canvas.md` — value curve divergence suggesting new space
  - `research/positioning.md` — existing positioning to build upon

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

- Read `research/competitive-analysis.md` — existing categories, how competitors position
- Read `research/icp.md` — customer language about the problem space
- Read `research/journey-map.md` — where category expectations break down
- Read prior framework outputs if available

### 2. Category Diagnosis

Determine which category strategy is appropriate by evaluating three options:

**Existing category** — Compete within a known category:
- When: the category is well-understood, you can win on a specific dimension, buyers already search for this category
- Risk: you inherit comparison criteria set by the category leader

**Subcategory** — Carve a niche within an existing category:
- When: you serve a specific segment much better than generic solutions, the parent category is recognized but you need differentiation
- Risk: the niche may be too small or the parent category absorbs it

**New category** — Create a category that doesn't exist yet:
- When: existing categories constrain your value, buyers are frustrated by current framing, a genuine market shift enables new thinking
- Risk: expensive, slow, requires sustained investment in education

Use WebSearch (3-5 queries) to validate category landscape:
- "[domain] market categories", "[domain] Gartner/Forrester category"
- "[problem space] new category", "[competitor] category creation"
- "is [category] a real category", "[domain] category evolution"

Present diagnosis. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "Based on evidence, I recommend [existing/subcategory/new] category strategy because [reasons]. The alternatives have these trade-offs: [trade-offs]. Does this match your ambition and resources?"

### 3. Category Naming (if subcategory or new)

If the diagnosis recommends subcategory or new category:

- Generate 5-7 candidate category names
- Evaluate each against criteria:
  - **Descriptive**: Does it explain what the category does?
  - **Differentiated**: Does it clearly separate from adjacent categories?
  - **Memorable**: Is it easy to say, search, and remember?
  - **Expandable**: Can it grow beyond the initial product?
  - **Not already claimed**: Is another company using this name?

Use WebSearch to validate name availability and adjacency.

Present candidates. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "Here are candidate category names with trade-offs. Which resonates? Any naming constraints I should know?"

### 4. Point of View (POV) Development

Develop the category POV — the worldview that makes this category inevitable:

- **The old way**: How things work today (and why it's broken)
- **The shift**: What's changing that makes the old way untenable
- **The new way**: How things should work (the category vision)
- **The proof**: Evidence that the shift is real and happening now

The POV should:
- Be bigger than the product (it's about the category, not features)
- Create urgency (why now, not later)
- Resonate emotionally (not just rationally)
- Be defensible (rooted in real trends, not manufactured urgency)

### 5. Ecosystem Mapping

Map the ecosystem that would surround this category:

- **Adjacent categories**: What categories does this border?
- **Potential allies**: Who benefits from this category existing?
- **Potential partners**: What complementary products would integrate?
- **Analysts/influencers**: Who would cover this category?
- **Ecosystem maturity**: How developed is the supporting infrastructure?

### 6. Assess Category Creation Feasibility

If recommending new category, honestly assess:

| Factor | Status | Evidence |
|--------|--------|----------|
| Market timing | [Early/Right/Late] | [why] |
| Company resources | [Sufficient/Insufficient] | [what's needed] |
| Buyer readiness | [Ready/Emerging/Premature] | [signals] |
| Competition response | [Likely follow/Likely ignore/Will fight] | [why] |
| Education investment | [Low/Medium/High] | [what's required] |

### 7. Write Output

Only after user approval.

## Output

### `research/positioning-category-design.md` (or `research/{slug}/positioning-category-design.md`)

```markdown
# Category Design Analysis

> Based on: research/competitive-analysis.md, research/icp.md, research/journey-map.md
> Date: [current date]
> Methodology: Play Bigger Category Design

## Category Diagnosis

**Recommendation**: [Existing / Subcategory / New Category]
**Confidence**: [Strong / Moderate / Weak]
**Rationale**: [2-3 sentences]

### Options Evaluated

| Strategy | Fit | Pros | Cons | Evidence |
|----------|-----|------|------|----------|
| Existing: [name] | [H/M/L] | [pros] | [cons] | [source] |
| Subcategory: [name] | [H/M/L] | [pros] | [cons] | [source] |
| New: [name] | [H/M/L] | [pros] | [cons] | [source] |

## Category Name (if subcategory or new)

**Recommended name**: [name]
**Alternatives considered**: [list with reasons rejected]

### Name Evaluation

| Criterion | Score | Notes |
|-----------|-------|-------|
| Descriptive | [1-5] | [notes] |
| Differentiated | [1-5] | [notes] |
| Memorable | [1-5] | [notes] |
| Expandable | [1-5] | [notes] |
| Available | [Y/N] | [notes] |

## Point of View

### The Old Way
[How things work today — the broken status quo]

### The Shift
[What's changing — the trend that makes the old way untenable]

### The New Way
[The category vision — how things should work]

### The Proof
[Evidence the shift is real: market signals, customer behavior, technology trends]

## Ecosystem Map

### Adjacent Categories
- [category] — [relationship]

### Potential Allies
- [company/community] — [why they benefit]

### Integration Partners
- [product/platform] — [complementary value]

### Category Feasibility (new category only)

| Factor | Status | Evidence |
|--------|--------|----------|
| Market timing | [status] | [evidence] |
| Resources | [status] | [evidence] |
| Buyer readiness | [status] | [evidence] |
| Competition response | [status] | [evidence] |
| Education cost | [status] | [evidence] |

## Implications for Positioning Synthesis

[How this category design analysis should influence the final positioning — what market category to declare, how to frame the category in messaging, and what POV narrative to lead with]
```

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable work goes in `tasks/todo.md`.
- Human-only external actions go in `tasks/manual-todo.md` with blocking/dependency annotations.
- Condition-gated records go in `tasks/record-todo.md`.
- Cadence-based reviews go in `tasks/recurring-todo.md`.

## Constraints

- **Intermediate artifact only.** This produces `research/positioning-category-design.md`, not the canonical `research/positioning.md`.
- **Honest about category creation costs.** New categories require years of investment. Don't recommend lightly.
- **POV must be bigger than the product.** If the POV is just "our product is better," it's not a category POV.
- **Naming requires validation.** Don't recommend names without checking they're not already claimed.
- **Present before writing.** Never write output files until findings are validated.
- **Category strategy must match resources.** A bootstrapped startup cannot create a new category the same way a funded company can.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/category-design-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
