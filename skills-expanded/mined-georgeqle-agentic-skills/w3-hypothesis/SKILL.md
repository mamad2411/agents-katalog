---
name: w3-hypothesis
description: Schwartzfarb W3 — define WHO/WHAT/WHY for each ICP candidate, generate disproval hypotheses, and validate via targeted research
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: customer-discovery
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# W3 Hypothesis — Schwartzfarb WHO/WHAT/WHY Analysis

## Parent Orchestrator Routing

Run only through the parent orchestrator `$customer-discovery` as part of its Research Session Loop. If the user needs to continue pending framework work, tell them to start a fresh Codex session and re-invoke `$customer-discovery` with the same product/research path argument when present, for example `$customer-discovery research/afps-tracker`.

Do not ask users to invoke this framework directly or with a path-shaped child framework command. Do not emit downstream routing labels, child-framework commands, execution-loop commands, or downstream skill recommendations from this framework subskill.

## Terminal Handoff Contract

When this framework is run inline and stops on its findings `review` page, the terminal response must end with:

```markdown
## Next Work
Review the framework findings page, compile YAML, and paste it into a session invoking the parent skill. The parent will consume that YAML, write the approved intermediate, and recalculate whether another framework or synthesis is next.

## Invoke With YAML
$customer-discovery
```

Use the same product/research path argument when present. Do not decide from inside the framework whether the next parent run executes another framework or synthesis; the parent orchestrator recalculates that from the run manifest and canonical-intermediate files after approval.

The findings `review` page must also include `agent_routing` in bottom compiled YAML with this parent-owned shape:

```yaml
agent_routing:
  workflow: pattern-a-research-loop
  parent_skill: customer-discovery
  command: "$customer-discovery research/{slug}"
  product_path: research/{slug}
  gate_owner: parent-orchestrator
  gate_type: framework-findings
  framework_slug: w3-hypothesis
  framework_mode: inline-subskill
  run_manifest: research/{slug}/_working/customer-discovery-run.yaml
  next_resolution: parent-resolves-from-yaml-and-filesystem
```

Omit `product_path` in flat mode, keep `command` identical to the parent command shown under `## Invoke With YAML`, and never replace it with a child framework path command. The parent consumes this YAML, writes the approved intermediate, archives the working packet/page, and recalculates the next state.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language while scope or artifact approval is pending. While the framework findings page is in `review`, use only the parent-owned terminal handoff sections above. Parent-loop continuation is not downstream routing, but it must name only `$customer-discovery`. Downstream routing belongs to parent synthesis only after approved synthesis artifacts are written or updated.

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

- **Hard**: ICP candidates from orchestrator working packet (`research/_working/preliminary-customer-discovery-research.md`) or `research/icp.md` (or `research/{slug}/icp.md`) must exist. If neither exists, tell the user to run `$customer-discovery` first and stop.
- **Soft**: `research/competitive-analysis.md`, `research/customer-feedback.md`, idea brief, specs, and codebase context when available.

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

- Read ICP candidates from orchestrator working packet (`research/_working/preliminary-customer-discovery-research.md`) or `research/icp.md`
- Read idea brief (`research/idea-scope-brief.md`) if it exists
- Read `research/competitive-analysis.md` if it exists
- Read `research/customer-feedback.md` if it exists
- Read CLAUDE.md, README for product context
- Scan codebase and existing research for additional signal

### 2. Define W3 for Each ICP Candidate

For each ICP candidate, construct the three-variable hypothesis:

**WHO** — narrowly defined buyer/customer:
- Demographics: age, location, education, income level
- Firmographics: company size, stage, industry, revenue, funding status
- Psychographics: values, motivations, risk tolerance, decision-making style
- Role/title, budget authority, buying power
- Behavioral patterns: where they spend time, what they read, who they trust

**WHAT** — what they're actually buying (the outcome, not the product):
- The specific problem being solved
- The outcome or transformation they expect
- What success looks like in their words
- The difference between what they say they want and what they actually need
- How they measure whether they got what they paid for

**WHY** — the business driver and measurable impact:
- Primary business driver: revenue growth, cost reduction, compliance, competitive pressure, efficiency
- Measurable impact: quantifiable benefit they expect
- Urgency level: why now, not later
- Macro trends or market forces creating the window
- What happens if they do nothing (cost of inaction)

### 3. Generate Disproval Hypotheses

For each W in each candidate's W3, generate 2-3 hypotheses that would **disprove** the assumption. The goal is falsification, not confirmation.

- **WHO disproval**: "If our WHO is wrong, we'd expect to see [specific evidence]. For example: the actual buyer is a different role, the company size doesn't match, the budget holder is someone else."
- **WHAT disproval**: "If our WHAT is wrong, we'd expect to see [specific evidence]. For example: customers describe the problem differently, they measure success by different metrics, the outcome they want is adjacent but distinct."
- **WHY disproval**: "If our WHY is wrong, we'd expect to see [specific evidence]. For example: the urgency driver is different, the business case doesn't hold at their scale, the macro trend is weaker than assumed."

### 4. Targeted Research

Run WebSearch queries designed to test each disproval hypothesis:
- Search for evidence that contradicts each W assumption
- Search for evidence that supports each W assumption
- Log every query and its key findings
- Look for competitor positioning that implies a different WHO/WHAT/WHY
- Look for community discussions, job postings, industry reports that reveal actual buyer behavior
- Prioritize disconfirming evidence — confirmation bias is the enemy

### 5. Score Hypothesis Confidence

For each ICP candidate, score each W dimension:

- **Strong**: multiple independent sources support the assumption; disproval hypotheses tested and no significant contradicting evidence found
- **Moderate**: some supporting evidence; one or more disproval hypotheses partially supported; key uncertainties remain
- **Weak**: limited evidence; disproval hypotheses found supporting evidence; significant risk the assumption is wrong

Calculate an overall candidate confidence based on the weakest dimension — a candidate is only as strong as its weakest W.

### 6. Validate with User

Present W3 definitions, disproval evidence, and confidence scores. Ask for corrections, missing context, and whether any candidates should be eliminated or refined.

## Output

### `research/customer-discovery-w3-hypothesis.md` (or `research/{slug}/customer-discovery-w3-hypothesis.md`)

```markdown
# W3 Hypothesis Analysis

> Based on: [sources]
> Date: [current date]
> Methodology: Schwartzfarb W3 (WHO/WHAT/WHY)

## ICP Candidate: [Name]

### WHO
[Narrow buyer definition — demographics, firmographics, psychographics, role, budget authority]

### WHAT
[What they're actually buying — the outcome, not the product]

### WHY
[Business driver and measurable impact, urgency, macro trends]

### Disproval Evidence
| Hypothesis | Evidence For | Evidence Against | Confidence |
|------------|-------------|-----------------|------------|
| WHO: [specific disproval hypothesis] | [supporting evidence] | [contradicting evidence] | Strong/Moderate/Weak |
| WHAT: [specific disproval hypothesis] | [supporting evidence] | [contradicting evidence] | Strong/Moderate/Weak |
| WHY: [specific disproval hypothesis] | [supporting evidence] | [contradicting evidence] | Strong/Moderate/Weak |

## ICP Candidate: [Name 2]
...

## Cross-Candidate Comparison
| Candidate | WHO Confidence | WHAT Confidence | WHY Confidence | Overall |
|-----------|---------------|-----------------|----------------|---------|
| [name] | Strong/Moderate/Weak | Strong/Moderate/Weak | Strong/Moderate/Weak | Strong/Moderate/Weak |

## Research Log
| Query | Key Findings | Disproval Target |
|-------|-------------|-----------------|
| [search query] | [what was found] | [which W hypothesis this tested] |

## Evidence Matrix
| Claim | Evidence Source | Evidence Type | Confidence |
|-------|---------------|---------------|------------|
| [claim] | [source] | Observed/Inferred/Hypothesized | High/Medium/Low |
```

## Constraints

- Ground every W3 definition and confidence score in evidence from ICP candidates, research, specs, feedback, or codebase.
- Prioritize disconfirming evidence — the framework demands falsification, not confirmation.
- Do not prescribe UI or architecture — describe the customer hypothesis, not the solution.
- Present findings before writing.
- Do not overwrite existing output without asking the user first.
- This is a child framework skill in the `customer-discovery` Research Session Loop. Do not emit cross-skill or downstream routing from framework stops, and do not recommend execution-loop commands or path-shaped child framework invocations. Inline framework handoff sections must name only the parent command `$customer-discovery`.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/w3-hypothesis-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
