---
name: jtbd-positioning
description: Jobs-to-be-Done positioning analysis — identify primary job, map functional/social/emotional dimensions, position around job outcome
type: research
version: v0.9
invocation: sub-skill
parent: positioning
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# JTBD Positioning — Jobs-to-be-Done Analysis

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

Applies Clayton Christensen's Jobs-to-be-Done framework to positioning. Instead of positioning around features or competitive differences, positions the product around the *job outcome* the customer is trying to achieve. Produces an intermediate artifact that feeds into the parent `$positioning` synthesis.

## Prerequisites

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `$customer-discovery` first and stop.
- **Hard**: `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) must exist. If not, tell the user to run `$competitive-analysis` first and stop.
- **Hard**: `research/journey-map.md` (or `research/{slug}/journey-map.md`) must exist. If not, tell the user to run `$journey-map` first and stop.
- **Soft**: Read if they exist:
  - `research/customer-feedback.md` — real language about what customers hire the product to do
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

- Read `research/icp.md` — segments, pain points, trigger events
- Read `research/competitive-analysis.md` — how alternatives frame themselves
- Read `research/journey-map.md` — where value is delivered, switching triggers
- Read `research/customer-feedback.md` if it exists — actual hiring/firing language

### 2. Identify the Primary Job

Research and determine the core job the customer is trying to get done:

- Use WebSearch with 3-5 queries targeting job language in the domain
- Distinguish the **core functional job** from related consumption-chain jobs
- Frame as: "When [situation], I want to [motivation], so I can [expected outcome]"
- Identify the job at the right level of abstraction — not too broad (meaningless), not too narrow (feature-level)

Validate with user. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "Here is the primary job the evidence supports. Is the abstraction level right? Are there competing job framings I should consider?"

### 3. Map Job Dimensions

For the primary job, map three dimensions:

**Functional dimension** — What the customer is practically trying to accomplish:
- Core steps in getting the job done
- Speed, accuracy, reliability requirements
- Where current solutions break down

**Social dimension** — How the customer wants to be perceived:
- Professional identity alignment
- Team/peer perception
- Status and credibility implications

**Emotional dimension** — How the customer wants to feel:
- Confidence and control
- Reduced anxiety or frustration
- Sense of progress

### 4. Identify Job Outcome Metrics

Define success metrics from the customer's perspective (not product metrics):
- **Speed**: How quickly can the job be completed?
- **Accuracy**: How reliably does the job get done right?
- **Effort**: How much work does the customer have to put in?
- **Satisfaction**: How good does the outcome feel?

Map where alternatives fail on these metrics.

### 5. Position Around Job Outcome

Synthesize positioning that frames the product as the best way to achieve the desired job outcome:

- What is the job the product is hired for?
- What makes this product uniquely suited to the job?
- What outcome does the customer achieve that alternatives cannot deliver?
- Which dimension (functional/social/emotional) is the strongest positioning angle?

Validate with user. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "This JTBD positioning emphasizes [dimension]. Does that match where you see the strongest pull from customers?"

### 6. Write Output

Only after user approval.

## Output

### `research/positioning-jtbd.md` (or `research/{slug}/positioning-jtbd.md`)

```markdown
# JTBD Positioning Analysis

> Based on: research/icp.md, research/competitive-analysis.md, research/journey-map.md
> Date: [current date]
> Methodology: Jobs-to-be-Done (Clayton Christensen / Tony Ulwick)

## Primary Job Statement

When [situation], I want to [motivation], so I can [expected outcome].

## Job Dimensions

### Functional
| Step | Current Solution | Pain Point | Our Advantage |
|------|-----------------|------------|---------------|
| [step] | [how done today] | [what breaks] | [how we're better] |

### Social
- [social dimension 1]
- [social dimension 2]

### Emotional
- [emotional dimension 1]
- [emotional dimension 2]

## Outcome Metrics

| Metric | Customer Need | Alternative Performance | Our Performance |
|--------|--------------|------------------------|-----------------|
| Speed | [need] | [how alternatives do] | [how we do] |
| Accuracy | [need] | [performance] | [performance] |
| Effort | [need] | [performance] | [performance] |

## Positioning Angle

**Lead dimension**: [Functional / Social / Emotional]
**Job outcome framing**: [one sentence: how to position around the job outcome]
**Evidence strength**: [Strong / Moderate / Weak — with justification]

## Competitive Alternatives by Job

| Alternative | Which Job It Serves | Where It Fails |
|-------------|--------------------|--------------------|
| [alternative] | [job framing] | [gap] |

## Implications for Positioning Synthesis

[How this JTBD analysis should influence the final positioning statement — what it suggests for market category, target segment, and key differentiator]
```

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable work goes in `tasks/todo.md`.
- Human-only external actions go in `tasks/manual-todo.md` with blocking/dependency annotations.
- Condition-gated records go in `tasks/record-todo.md`.
- Cadence-based reviews go in `tasks/recurring-todo.md`.

## Constraints

- **Intermediate artifact only.** This produces `research/positioning-jtbd.md`, not the canonical `research/positioning.md`.
- **Requires journey evidence.** JTBD positioning without understanding the customer journey is speculative.
- **Job abstraction level matters.** Challenge yourself: is the job too broad or too narrow?
- **Present before writing.** Never write output files until findings are validated.
- **Customer language preferred.** Use actual customer words from feedback/interviews when available.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/jtbd-positioning-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
