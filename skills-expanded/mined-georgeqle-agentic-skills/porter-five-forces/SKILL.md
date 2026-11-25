---
name: porter-five-forces
description: Porter's Five Forces competitive analysis - industry structure, rivalry, substitutes, entrants, buyer power, and supplier power
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: competitive-analysis
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Porter's Five Forces - Competitive Structure Analysis

## Parent Orchestrator Routing

Run only through the parent orchestrator `$competitive-analysis` as part of its Research Session Loop. If the user needs to continue pending framework work, tell them to start a fresh Codex session and re-invoke `$competitive-analysis` with the same product/research path argument when present, for example `$competitive-analysis research/afps-tracker`.

Do not ask users to invoke this framework directly or with a path-shaped child framework command. Do not emit downstream routing labels, child-framework commands, execution-loop commands, or downstream skill recommendations from this framework subskill.

## Terminal Handoff Contract

When this framework is run inline and stops on its findings `review` page, the terminal response must end with:

```markdown
## Next Work
Review the framework findings page, compile YAML, and paste it into a session invoking the parent skill. The parent will consume that YAML, write the approved intermediate, and recalculate whether another framework or synthesis is next.

## Invoke With YAML
$competitive-analysis
```

Use the same product/research path argument when present. Do not decide from inside the framework whether the next parent run executes another framework or synthesis; the parent orchestrator recalculates that from the run manifest and canonical-intermediate files after approval.

The findings `review` page must also include `agent_routing` in bottom compiled YAML with this parent-owned shape:

```yaml
agent_routing:
  workflow: pattern-a-research-loop
  parent_skill: competitive-analysis
  command: "$competitive-analysis research/{slug}"
  product_path: research/{slug}
  gate_owner: parent-orchestrator
  gate_type: framework-findings
  framework_slug: porter-five-forces
  framework_mode: inline-subskill
  run_manifest: research/{slug}/_working/competitive-analysis-run.yaml
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

## Prerequisites

- **Hard**: Parent context from `research/_working/preliminary-competitive-analysis-research.md` or `research/{slug}/_working/preliminary-competitive-analysis-research.md`. If absent, read `research/icp.md` or `research/{slug}/icp.md` plus repo context; if neither exists, tell the user to run `$competitive-analysis` first and stop.
- **Soft**: Existing `research/competitive-analysis-*.md`, `research/customer-feedback.md`, `research/journey-map.md`, specs, and codebase context.

## Product-Path Scope Resolution

Use the parent `competitive-analysis` product-path scope when present. Otherwise resolve scope by reading `research/.progress.yaml`, selecting active non-archived product paths, and writing under `research/{slug}/` only when that path is active or explicitly named.

## Process

1. Load parent context and identify the relevant category, buyer/customer frame, seeded competitors, and source gaps.
2. Use web search to validate the market boundary and identify evidence for each force.
3. Assess:
   - competitive rivalry
   - threat of new entrants
   - threat of substitutes and DIY alternatives
   - buyer/customer power
   - supplier/platform/channel power
4. Score each force as low, moderate, or high pressure with evidence and confidence.
5. Identify the structural constraints, exploitable gaps, and risks that the parent synthesis should carry forward.
6. Present findings before writing and incorporate factual corrections.

## Output

### `research/competitive-analysis-porter-five-forces.md` (or `research/{slug}/competitive-analysis-porter-five-forces.md`)

```markdown
# Porter's Five Forces Analysis

> Based on: [parent context, sources]
> Date: [current date]
> Methodology: Porter's Five Forces

## Market Boundary
[Category, buyer frame, and competitors included/excluded]

## Force Assessment
| Force | Pressure | Evidence | Confidence | Implication |
|-------|----------|----------|------------|-------------|
| Rivalry | Low/Moderate/High | [sources] | High/Medium/Low | [what synthesis should consider] |
| New Entrants | Low/Moderate/High | [sources] | High/Medium/Low | [implication] |
| Substitutes | Low/Moderate/High | [sources] | High/Medium/Low | [implication] |
| Buyer Power | Low/Moderate/High | [sources] | High/Medium/Low | [implication] |
| Supplier Power | Low/Moderate/High | [sources] | High/Medium/Low | [implication] |

## Structural Opportunities
[White-space openings created by force dynamics]

## Structural Risks
[Forces that could undermine the product or category thesis]

## Evidence Matrix
| Claim | Source | Evidence Type | Confidence |
|-------|--------|---------------|------------|
```

## Constraints

- Every competitor or market fact must be source-backed.
- Prefer recent sources from the last 12 months and flag older evidence.
- Do not recommend product features, positioning, architecture, or downstream skills.
- This is a sub-skill; do not emit downstream routing labels or command recommendations.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/porter-five-forces-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
