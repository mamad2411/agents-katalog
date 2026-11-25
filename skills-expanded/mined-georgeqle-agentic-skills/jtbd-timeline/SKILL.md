---
name: jtbd-timeline
description: Moesta/Switch JTBD timeline — map first thought→passive→active→deciding→consuming→satisfaction with push/pull/anxiety/habit forces
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: journey-map
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# JTBD Timeline — Moesta/Switch Analysis

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
  framework_slug: jtbd-timeline
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
- Read `research/competitive-analysis.md` if it exists — what alternatives customers switch from/to
- Read `research/customer-feedback.md` if it exists — switching stories, frustrations, trigger language
- Read CLAUDE.md, README for product context

### 2. Map the Switching Timeline

Reconstruct the customer's decision timeline using Moesta's six stages:

**First Thought**: The moment the customer first realizes something isn't working. What triggered awareness? What was the catalyzing event?

**Passive Looking**: The customer is aware but not actively searching. They notice alternatives, read about options, but haven't committed to change. What keeps them in passive mode? What would accelerate them?

**Active Looking**: The customer is now deliberately evaluating alternatives. What criteria are they using? What channels are they searching? Who are they asking?

**Deciding**: The customer has narrowed options and is making a choice. What is the final trigger? What reassurance do they need? What objections remain?

**Consuming**: The customer has switched and is using the new solution. What does the first experience look like? When does buyer's remorse or confirmation set in?

**Satisfaction**: The customer evaluates whether the switch was worth it. Are they better off? Would they recommend? Would they switch again?

### 3. Map the Four Forces

For each timeline stage, identify the four forces that drive or resist change:

**Push of the current situation** (drives change):
- What frustrations, limitations, or failures push the customer away from their current solution?
- What is getting worse over time?
- What events amplify the push?

**Pull of the new solution** (drives change):
- What about the new solution attracts the customer?
- What outcomes or capabilities are they drawn to?
- What promises or proof creates pull?

**Anxiety of the new solution** (resists change):
- What worries the customer about switching?
- What could go wrong?
- What uncertainty exists about the new solution?
- What learning curve or migration cost is feared?

**Habit of the current situation** (resists change):
- What keeps the customer with their current solution despite frustrations?
- What workflows, integrations, or muscle memory create inertia?
- What switching costs (real or perceived) exist?

### 4. Identify Force Imbalances

Analyze where forces are misaligned:
- Where is push strong but pull weak? (customer wants to leave but has nowhere compelling to go)
- Where is pull strong but anxiety blocks? (customer wants the new solution but fears the switch)
- Where is everything aligned but habit wins? (customer should switch but inertia is too strong)
- What is the minimum force combination needed to trigger switching?

### 5. Identify the Hiring Criteria

What the customer is actually "hiring" the product to do:
- Functional job: what task or outcome they need accomplished
- Social job: how they want to be perceived by others
- Emotional job: how they want to feel

### 6. Validate with User

Present the timeline, forces analysis, and hiring criteria. Ask for corrections, missing stages, and product-specific context.

## Output

### `research/journey-map-jtbd-timeline.md` (or `research/{slug}/journey-map-jtbd-timeline.md`)

```markdown
# JTBD Switching Timeline

> Based on: research/icp.md[, other evidence]
> Date: [current date]
> Methodology: Moesta/Switch JTBD Timeline

## Switching Timeline

| Stage | Customer State | Duration | Key Evidence |
|-------|---------------|----------|-------------|
| First Thought | [catalyzing event] | [timeframe] | [source] |
| Passive Looking | [awareness state] | [timeframe] | [source] |
| Active Looking | [evaluation criteria] | [timeframe] | [source] |
| Deciding | [decision trigger] | [timeframe] | [source] |
| Consuming | [first experience] | [timeframe] | [source] |
| Satisfaction | [outcome evaluation] | [timeframe] | [source] |

## Four Forces Analysis

### Push of Current Situation
| Force | Intensity | Stage Most Active | Evidence |
|-------|-----------|-------------------|----------|
| [frustration/failure] | High/Medium/Low | [stage] | [source] |

### Pull of New Solution
| Force | Intensity | Stage Most Active | Evidence |
|-------|-----------|-------------------|----------|
| [attraction/outcome] | High/Medium/Low | [stage] | [source] |

### Anxiety of New Solution
| Force | Intensity | Stage Most Active | Evidence |
|-------|-----------|-------------------|----------|
| [worry/uncertainty] | High/Medium/Low | [stage] | [source] |

### Habit of Current Situation
| Force | Intensity | Stage Most Active | Evidence |
|-------|-----------|-------------------|----------|
| [inertia/switching cost] | High/Medium/Low | [stage] | [source] |

## Force Imbalances

| Imbalance | Stage | Implication | Intervention |
|-----------|-------|-------------|-------------|
| [type] | [stage] | [what this means] | [what could shift it] |

## Hiring Criteria

### Functional Job
[What task or outcome they need]

### Social Job
[How they want to be perceived]

### Emotional Job
[How they want to feel]

## Evidence Matrix

| Claim | Evidence Source | Evidence Type | Confidence |
|-------|---------------|---------------|------------|
| [claim] | [source] | Observed/Inferred/Hypothesized | High/Medium/Low |
```

## Constraints

- Ground every timeline stage and force in ICP, research, specs, feedback, or codebase evidence.
- Do not prescribe UI or architecture — describe the switching journey, not the solution.
- Present findings before writing.
- Do not overwrite existing output without asking the user first.
- This is a sub-skill; do not emit downstream routing labels or command recommendations.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/jtbd-timeline-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
