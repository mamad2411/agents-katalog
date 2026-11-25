---
name: jtbd-needs
description: Ulwick/Christensen JTBD — identify jobs, map desired outcomes, score importance vs satisfaction, and segment ICP candidates by unmet needs
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: customer-discovery
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# JTBD Needs — Ulwick/Christensen Outcome-Driven Innovation

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
  framework_slug: jtbd-needs
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

### 2. Identify Jobs-to-be-Done

For each ICP candidate, identify the full job landscape:

**Functional jobs** — tasks and outcomes they need accomplished:
- Core tasks they hire a solution to perform
- Desired outcomes for each task (measurable results)
- Related tasks that precede, follow, or co-occur with the core job
- Frequency and context of job execution

**Social jobs** — how they want to be perceived:
- Professional reputation goals
- Peer perception and status signals
- Team/org perception of their decisions
- Industry credibility and thought leadership

**Emotional jobs** — how they want to feel:
- Confidence and control over outcomes
- Reduced anxiety about risks or unknowns
- Satisfaction and sense of progress
- Freedom from tedious or frustrating work

**Related jobs** — adjacent jobs that create context:
- Jobs performed immediately before and after
- Jobs that share the same workflow or trigger
- Jobs delegated to other roles that affect this one
- Jobs that compete for the same time/attention

**Consumption chain jobs** — jobs around acquiring, using, maintaining the solution:
- Evaluate and select solutions
- Onboard and learn the solution
- Integrate with existing workflow
- Maintain, update, and extend over time
- Migrate away when the job changes

### 3. Map Desired Outcomes

For each job, write Ulwick outcome statements following the canonical format:

`[Direction of improvement] + [performance metric] + [object of control] + [contextual clarifier]`

Direction of improvement: Minimize, Maximize, Increase, Reduce, Eliminate, Optimize

Examples:
- "Minimize the time it takes to identify qualified leads in a new market segment"
- "Reduce the likelihood of misallocating budget to underperforming channels"
- "Maximize the percentage of outreach messages that receive a response"
- "Minimize the number of tools required to complete end-to-end campaign analysis"

Write 8-15 outcome statements per core functional job, 3-5 per social/emotional job.

### 4. Score Importance & Satisfaction

For each outcome statement, score based on available evidence (research, feedback, competitive analysis, codebase signals):

- **Importance** (1-10): How important is achieving this outcome to the ICP candidate?
- **Current Satisfaction** (1-10): How well do existing solutions satisfy this outcome?

Calculate **Opportunity Score**: `Importance + max(Importance - Satisfaction, 0)`

Classify each outcome:
- **Underserved** (opportunity score ≥ 12): high importance, low satisfaction — prime innovation targets
- **Appropriately served** (opportunity score 8-11): adequate current solutions exist
- **Overserved** (opportunity score < 8): low importance or high satisfaction — potential to simplify/reduce

### 5. Segment by Unmet Needs

Cluster ICP candidates by shared patterns of underserved outcomes:

- Identify candidates with similar underserved outcome clusters
- Define natural segments based on shared unmet needs (not demographics)
- Map cross-segment patterns: outcomes underserved across all candidates
- Identify segment-specific opportunity areas unique to each cluster
- Rank segments by total addressable opportunity (sum of opportunity scores for underserved outcomes)
- Note which segments align with or diverge from demographic/firmographic ICP boundaries

### 6. Validate with User

Present jobs, outcomes, opportunity scores, and segment recommendations. Ask for corrections on:
- Job completeness: missing jobs or mischaracterized job importance
- Outcome accuracy: whether statements reflect real user language and priorities
- Scoring calibration: whether importance/satisfaction estimates match known reality
- Segment validity: whether proposed clusters reflect real behavioral differences

## Output

### `research/customer-discovery-jtbd-needs.md` (or `research/{slug}/customer-discovery-jtbd-needs.md`)

```markdown
# JTBD Needs Analysis

> Based on: [sources]
> Date: [current date]
> Methodology: Ulwick/Christensen Outcome-Driven Innovation

## ICP Candidate: [Name]

### Functional Jobs
| Job | Context | Frequency |
|-----|---------|-----------|
| [core task] | [when/where this job arises] | [how often] |

### Social & Emotional Jobs
| Type | Job | Evidence |
|------|-----|----------|
| Social | [how they want to be perceived] | [source] |
| Emotional | [how they want to feel] | [source] |

### Desired Outcomes & Opportunity Scores
| Outcome Statement | Job | Importance | Satisfaction | Opportunity Score | Classification |
|-------------------|-----|------------|--------------|-------------------|----------------|
| [direction] + [metric] + [object] + [context] | [parent job] | 1-10 | 1-10 | calculated | Underserved/Served/Overserved |

### Top Underserved Outcomes
1. [outcome] — Opportunity Score: [score]
2. [outcome] — Opportunity Score: [score]
3. [outcome] — Opportunity Score: [score]

## ICP Candidate: [Name 2]
...

## Opportunity Landscape
| Outcome | Candidate(s) | Importance | Satisfaction | Opportunity Score |
|---------|-------------|------------|--------------|-------------------|
| [outcome] | [who shares it] | [avg] | [avg] | [score] |

## Needs-Based Segments
### Segment: [Name]
- **Shared underserved outcomes**: [list]
- **ICP candidates in segment**: [list]
- **Total addressable opportunity**: [sum of opportunity scores]
- **Distinguishing characteristic**: [what unites them beyond demographics]

## Cross-Candidate Comparison
| Candidate | Top Underserved Outcome | Segment | Total Opportunity |
|-----------|------------------------|---------|-------------------|
| [name] | [highest-scoring outcome] | [segment] | [sum] |

## Evidence Matrix
| Claim | Evidence Source | Evidence Type | Confidence |
|-------|---------------|---------------|------------|
| [claim] | [source] | Observed/Inferred/Hypothesized | High/Medium/Low |
```

## Constraints

- Ground every job, outcome, and score in evidence from ICP candidates, research, specs, feedback, or codebase.
- Use Ulwick's canonical outcome statement format — do not shortcut to vague needs language.
- Prioritize underserved outcomes as innovation targets; do not optimize for overserved outcomes.
- Do not prescribe UI or architecture — describe the customer need, not the solution.
- Present findings before writing.
- Do not overwrite existing output without asking the user first.
- This is a child framework skill in the `customer-discovery` Research Session Loop. Do not emit cross-skill or downstream routing from framework stops, and do not recommend execution-loop commands or path-shaped child framework invocations. Inline framework handoff sections must name only the parent command `$customer-discovery`.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/jtbd-needs-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
