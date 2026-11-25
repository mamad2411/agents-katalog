---
name: experience-map
description: Adaptive Path experience map — emotional arc with doing/thinking/feeling layers, pain/delight moments, and channel transitions
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: journey-map
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Experience Map — Adaptive Path Analysis

## Parent Orchestrator Routing

Run only through the parent orchestrator `$journey-map` as part of its Research Session Loop. If the user needs to continue pending framework work, tell them to start a fresh Codex session and re-invoke `$journey-map` with the same product/research path argument when present, for example `$journey-map research/afps-tracker`.

Do not ask users to invoke this framework directly or with a path-shaped child framework command. Do not emit downstream routing labels, child-framework commands, execution-loop commands, or downstream skill recommendations from this framework subskill.

## Terminal Handoff Contract

When this framework is run inline and stops on its findings `review` page, the terminal response must end with:

```markdown
## Next Work
Review the framework findings page, compile YAML, and paste it into a session invoking the parent skill. The parent will consume that YAML, write the approved intermediate, and recalculate whether another framework or synthesis is next.

## Invoke With YAML
$journey-map
```

Use the same product/research path argument when present. Do not decide from inside the framework whether the next parent run executes another framework or synthesis; the parent orchestrator recalculates that from the run manifest and canonical-intermediate files after approval.

The findings `review` page must also include `agent_routing` in bottom compiled YAML with this parent-owned shape:

```yaml
agent_routing:
  workflow: pattern-a-research-loop
  parent_skill: journey-map
  command: "$journey-map research/{slug}"
  product_path: research/{slug}
  gate_owner: parent-orchestrator
  gate_type: framework-findings
  framework_slug: experience-map
  framework_mode: inline-subskill
  run_manifest: research/{slug}/_working/journey-map-run.yaml
  next_resolution: parent-resolves-from-yaml-and-filesystem
```

Omit `product_path` in flat mode, keep `command` identical to the parent command shown under `## Invoke With YAML`, and never replace it with a child framework path command. The parent consumes this YAML, writes the approved intermediate, archives the working packet/page, and recalculates the next state.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include downstream routing language. While the framework findings page is in `review`, use only the parent-owned terminal handoff sections above. Parent synthesis owns downstream routing only after approved synthesis artifacts are written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page so it renders the complete working-packet substance as structured HTML review UI: purpose-built sections, tables, matrices, gates, cards, and tier-appropriate charts or diagrams that preserve every packet section, finding, caveat, and decision detail without summary loss. Raw Markdown packet text may appear only as a supplemental source view after the rendered review UI; do not make a `Full Preliminary Packet` or `Full Working Packet` raw Markdown dump, giant `<pre><code>` block, link-only view, or source-only view the primary review surface. Include the evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. Push back clearly and cite the evidence when the user appears to misunderstand.
- For taste, prioritization, or subjective judgment calls: weigh user feedback heavily and adapt unless it conflicts with verified evidence.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Prerequisites

- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `$customer-discovery` first and stop.
- **Soft**: `research/competitive-analysis.md`, `research/customer-feedback.md`, specs, and codebase context when available.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`.

### 1. Load Context

- Read `research/icp.md` — ICP segments, pain points, trigger events
- Read `research/competitive-analysis.md` if it exists
- Read `research/customer-feedback.md` if it exists — emotional language, satisfaction drivers
- Read CLAUDE.md, README for product context

### 2. Define Experience Phases

Map the end-to-end experience across phases that span the full lifecycle, not just the product interaction. Typical phases: awareness, research, first contact, onboarding, core usage, deepening, advocacy/departure.

### 3. Map Doing Layer

For each phase, document what the person is actively doing:
- Actions taken (searching, comparing, signing up, configuring, using features)
- Tools and channels used
- Time spent per action
- Frequency and patterns

### 4. Map Thinking Layer

For each phase, document what the person is thinking:
- Questions they're asking themselves
- Comparisons and evaluations they're making
- Mental models they're building
- Expectations forming and shifting

### 5. Map Feeling Layer

For each phase, document the emotional state:
- Dominant emotion (frustrated, curious, confident, anxious, delighted)
- Emotional intensity (high/medium/low)
- Emotional trajectory (rising, falling, stable)
- Trigger for emotional shifts

### 6. Identify Pain and Delight Moments

Across all phases, identify:
- **Pain moments**: where negative emotion peaks — frustration, confusion, abandonment risk
- **Delight moments**: where positive emotion peaks — aha moments, unexpected value, mastery
- **Indifference zones**: where the experience is flat and forgettable
- **Channel transitions**: moments where the user switches between channels, devices, or contexts (these are high-friction by default)

### 7. Plot the Emotional Arc

Create the emotional journey curve:
- X-axis: experience phases (time/sequence)
- Y-axis: emotional valence (negative ↔ positive)
- Mark pain points, delight moments, and channel transitions on the curve
- Identify the overall arc shape (valley-then-peak, steady decline, roller-coaster, etc.)

### 8. Validate with User

Present the experience map and emotional arc. Ask for corrections, missing phases, and product-specific context.

## Output

### `research/journey-map-experience-map.md` (or `research/{slug}/journey-map-experience-map.md`)

```markdown
# Experience Map

> Based on: research/icp.md[, other evidence]
> Date: [current date]
> Methodology: Adaptive Path Experience Map

## Experience Phases

| Phase | Doing | Thinking | Feeling | Intensity |
|-------|-------|----------|---------|-----------|
| [phase] | [actions] | [thoughts] | [emotion] | High/Medium/Low |

## Emotional Arc

[Narrative description of the emotional trajectory across phases]

## Pain Moments

| Phase | Pain Point | Emotion | Intensity | Evidence |
|-------|-----------|---------|-----------|----------|
| [phase] | [description] | [emotion] | High/Medium/Low | [source] |

## Delight Moments

| Phase | Delight Point | Emotion | Intensity | Evidence |
|-------|--------------|---------|-----------|----------|
| [phase] | [description] | [emotion] | High/Medium/Low | [source] |

## Channel Transitions

| From | To | Phase | Friction Level | Evidence |
|------|-----|-------|---------------|----------|
| [channel] | [channel] | [phase] | High/Medium/Low | [source] |

## Evidence Matrix

| Claim | Evidence Source | Evidence Type | Confidence |
|-------|---------------|---------------|------------|
| [claim] | [source] | Observed/Inferred/Hypothesized | High/Medium/Low |
```

## Constraints

- Ground every experience element in ICP, research, specs, feedback, or codebase evidence.
- Do not prescribe UI or architecture — describe the experience, not the solution.
- Present findings before writing.
- Do not overwrite existing output without asking the user first.
- This is a sub-skill; do not emit downstream routing labels or command recommendations.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/experience-map-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
