---
name: moore-positioning
description: Geoffrey Moore positioning hypothesis — generate Moore template, map evidence per element, identify weakest link
type: research
version: v0.9
invocation: sub-skill
parent: positioning
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Moore Positioning — Geoffrey Moore Hypothesis

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

Applies Geoffrey Moore's positioning template from "Crossing the Chasm" to generate a structured positioning hypothesis, rigorously map evidence status for each element, and identify the weakest link that needs strengthening. This is a disciplined fill-in-the-blanks exercise that exposes gaps in positioning logic. Produces an intermediate artifact for the parent `$positioning` synthesis.

## Prerequisites

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `$customer-discovery` first and stop.
- **Hard**: `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) must exist. If not, tell the user to run `$competitive-analysis` first and stop.
- **Soft**: Read if they exist:
  - `research/journey-map.md` — context for trigger events and value delivery
  - `research/customer-feedback.md` — customer language for framing
  - `research/positioning-jtbd.md` — job framing to inform target customer
  - `research/positioning-strategic-canvas.md` — differentiation evidence
  - `research/positioning.md` — existing positioning to compare against

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

- Read `research/icp.md` — target customers, pain points, trigger events
- Read `research/competitive-analysis.md` — competitive landscape, alternatives
- Read any prior framework outputs (JTBD, strategic canvas) for evidence accumulation
- Read CLAUDE.md, README, key source files for product understanding

### 2. Generate Moore Template Hypothesis

Fill in the Geoffrey Moore positioning template:

> **For** [target customer]
> **who** [statement of need or opportunity]
> **the** [product name] **is a** [product category]
> **that** [key benefit — compelling reason to buy]
> **Unlike** [primary competitive alternative]
> **our product** [statement of primary differentiation]

Generate 2-3 candidate hypotheses with different framings:
- Vary the target customer specificity
- Vary the product category (existing, subcategory, new)
- Vary the competitive alternative anchor
- Vary the differentiation angle

### 3. Map Evidence Status Per Element

For each element of the template, assess evidence strength:

| Element | Content | Evidence Source | Confidence | Gap |
|---------|---------|----------------|------------|-----|
| Target customer | [from template] | [which research file] | Strong/Moderate/Weak | [what's missing] |
| Need/opportunity | [from template] | [source] | [confidence] | [gap] |
| Product category | [from template] | [source] | [confidence] | [gap] |
| Key benefit | [from template] | [source] | [confidence] | [gap] |
| Competitive alt. | [from template] | [source] | [confidence] | [gap] |
| Differentiation | [from template] | [source] | [confidence] | [gap] |

Use WebSearch (2-4 queries) to validate category framing and competitive alternative accuracy:
- "[product category] definition", "[primary alternative] positioning"
- "[category] market leader", "who competes with [alternative]"

### 4. Identify Weakest Link

Determine which template element has the weakest evidence or most problematic framing:

- **Target too broad?** — Positioning that works for everyone works for no one.
- **Need too generic?** — "Saves time" is not a positioning-grade need.
- **Category unclear?** — If buyers don't recognize the category, they can't evaluate.
- **Benefit not unique?** — If alternatives also claim this benefit, it's not positioning.
- **Wrong competitive anchor?** — If buyers don't actually consider this alternative, the "unlike" fails.
- **Differentiation unproven?** — Claims without evidence are aspirational, not positioning.

Present findings. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "The weakest link in this positioning hypothesis is [element] because [reason]. Which framing resonates best, and what evidence or insight can strengthen the weak link?"

### 5. Recommend Strongest Hypothesis

Select the strongest candidate and explain:
- Why it outperforms alternatives
- What evidence supports each element
- What remains unproven and how to resolve it
- How it compares to existing positioning (if any)

### 6. Write Output

Only after user approval.

## Output

### `research/positioning-moore.md` (or `research/{slug}/positioning-moore.md`)

```markdown
# Moore Positioning Hypothesis

> Based on: research/icp.md, research/competitive-analysis.md[, prior framework outputs]
> Date: [current date]
> Methodology: Geoffrey Moore "Crossing the Chasm" positioning template

## Recommended Hypothesis

> **For** [target customer]
> **who** [statement of need or opportunity]
> **the** [product name] **is a** [product category]
> **that** [key benefit — compelling reason to buy]
> **Unlike** [primary competitive alternative]
> **our product** [statement of primary differentiation]

## Evidence Map

| Element | Content | Source | Confidence | Gap |
|---------|---------|--------|------------|-----|
| Target customer | [content] | [source] | [S/M/W] | [gap or "none"] |
| Need/opportunity | [content] | [source] | [S/M/W] | [gap] |
| Product category | [content] | [source] | [S/M/W] | [gap] |
| Key benefit | [content] | [source] | [S/M/W] | [gap] |
| Competitive alt. | [content] | [source] | [S/M/W] | [gap] |
| Differentiation | [content] | [source] | [S/M/W] | [gap] |

## Weakest Link Analysis

**Weakest element**: [element name]
**Why it's weak**: [explanation]
**How to strengthen**: [specific action — more research, customer interviews, product changes]
**Risk if unresolved**: [what happens if this stays weak]

## Alternative Hypotheses Considered

### Hypothesis B
> [full Moore template]

**Why not recommended**: [reason]

### Hypothesis C
> [full Moore template]

**Why not recommended**: [reason]

## Implications for Positioning Synthesis

[How this Moore analysis should influence the final positioning — which elements are strongest, where the template reveals gaps, and what it suggests for the canonical positioning statement]
```

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable work goes in `tasks/todo.md`.
- Human-only external actions go in `tasks/manual-todo.md` with blocking/dependency annotations.
- Condition-gated records go in `tasks/record-todo.md`.
- Cadence-based reviews go in `tasks/recurring-todo.md`.

## Constraints

- **Intermediate artifact only.** This produces `research/positioning-moore.md`, not the canonical `research/positioning.md`.
- **Evidence mapping is non-negotiable.** Every template element must have a cited source and confidence level.
- **Multiple hypotheses required.** Never present a single option — the comparison reveals trade-offs.
- **Weakest link must be actionable.** Don't just identify the weakness — recommend how to fix it.
- **Present before writing.** Never write output files until findings are validated.
- **Accumulate prior framework evidence.** If JTBD or strategic canvas outputs exist, use them as evidence sources.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/moore-positioning-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
