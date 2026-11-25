---
name: four-forces
description: Moesta Four Forces of Progress — map Push, Pull, Anxiety, and Habit forces per ICP candidate to identify switching catalysts and barriers
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: customer-discovery
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Four Forces of Progress — Moesta Switching Analysis

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
  framework_slug: four-forces
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

### 2. Map Push Forces (Current Pain)

For each ICP candidate, identify what pushes them away from their current situation:

**Functional pain** — workflow and task failures:
- Tasks that take too long, fail frequently, or produce poor results
- Manual steps that should be automated
- Tools that don't integrate or require duplicate work
- Bottlenecks that block downstream work

**Financial pain** — cost and resource pressure:
- Direct costs of current solution (licenses, infrastructure, labor)
- Opportunity costs of time spent on workarounds
- Revenue lost due to current limitations
- Budget pressure or upcoming cost increases

**Emotional pain** — frustration and dissatisfaction:
- Frustration with unreliable or unintuitive tools
- Anxiety about errors, outages, or compliance gaps
- Embarrassment about manual or outdated processes
- Fatigue from repetitive or tedious work

**Social/organizational pain** — team and stakeholder friction:
- Complaints from team members or downstream consumers
- Management pressure to modernize or improve metrics
- Competitive embarrassment (peers using better tools)
- Hiring/retention difficulty due to outdated stack

Score each push factor: **Intensity** (1-10), **Frequency** (daily/weekly/monthly/quarterly), **Evidence strength** (Observed/Inferred/Hypothesized).

### 3. Map Pull Forces (New Solution Attraction)

For each ICP candidate, identify what attracts them toward a new solution:

**Functional pull** — capability and performance gains:
- New capabilities not possible with current solution
- Speed or quality improvements for existing workflows
- Better integration with existing tools and data
- Scalability for growth or new use cases

**Financial pull** — economic benefits:
- Lower total cost of ownership
- Faster time-to-value or ROI
- Revenue enablement (new capabilities that unlock revenue)
- Resource reallocation (time freed for higher-value work)

**Emotional pull** — aspirational and experiential benefits:
- Delight or excitement about a modern, elegant solution
- Confidence from better visibility, control, or reliability
- Pride in using a best-in-class tool
- Relief from eliminating a persistent frustration

**Social pull** — reputation and relationship benefits:
- Being seen as innovative or forward-thinking
- Better collaboration with team or partners
- Industry recognition or community belonging
- Improved hiring appeal (modern stack)

Score each pull factor: **Intensity** (1-10), **Specificity** (generic aspiration vs. concrete expectation), **Evidence strength** (Observed/Inferred/Hypothesized).

### 4. Map Anxiety Forces (Fear of Change)

For each ICP candidate, identify fears and concerns about switching:

**Performance anxiety** — will it actually work?
- Fear that the new solution won't deliver on promises
- Concern about edge cases, reliability, or data integrity
- Worry about losing capabilities they depend on today
- Skepticism based on past failed switches

**Implementation anxiety** — can we actually switch?
- Concern about migration complexity and data loss
- Fear of downtime or disruption during transition
- Worry about learning curve and team resistance
- Uncertainty about integration with existing systems

**Financial anxiety** — is it worth the risk?
- Fear of sunk cost if the switch fails
- Concern about hidden costs (migration, training, customization)
- Worry about being locked into a new vendor
- Budget approval uncertainty

**Social anxiety** — what will others think?
- Fear of blame if the switch goes wrong
- Concern about disrupting team workflows and relationships
- Worry about being the champion of a failed initiative
- Uncertainty about organizational buy-in

Score each anxiety factor: **Intensity** (1-10), **Addressability** (how easily can this concern be mitigated?), **Evidence strength** (Observed/Inferred/Hypothesized).

### 5. Map Habit Forces (Status Quo Inertia)

For each ICP candidate, identify what keeps them in their current situation:

**Behavioral habits** — ingrained workflows and muscle memory:
- Daily routines built around current tools
- Keyboard shortcuts, templates, and automation already configured
- Mental models and heuristics tuned to current system
- Workarounds that have become second nature

**Organizational habits** — institutional inertia:
- Processes and SOPs built around current tools
- Training materials and onboarding flows that assume current stack
- Compliance or audit trails tied to current system
- Vendor relationships and contract obligations

**Emotional habits** — comfort and identity:
- Sense of mastery and competence with current tools
- Identity tied to current way of working
- Comfort of the familiar despite known flaws
- "Good enough" rationalization

**Switching costs** — tangible barriers to change:
- Data migration effort and risk
- Retraining time for team
- Integration rebuilding with other systems
- Parallel running period requirements

Score each habit factor: **Intensity** (1-10), **Disruption cost** (Low/Medium/High — effort to overcome), **Evidence strength** (Observed/Inferred/Hypothesized).

### 6. Analyze Force Balance

For each ICP candidate, synthesize the four forces:

**Net force calculation:**
- **Driving forces** = Push intensity + Pull intensity
- **Restraining forces** = Anxiety intensity + Habit intensity
- **Net switching momentum** = Driving forces - Restraining forces

**Force balance classification:**
- **Strong switch signal** (net > +10): Driving forces clearly dominate — candidate is actively looking to switch
- **Moderate switch signal** (net +3 to +10): Driving forces lead but barriers are significant — candidate needs help overcoming anxiety/habit
- **Stalled** (net -2 to +2): Forces roughly balanced — candidate is aware of problems but won't act without a catalyst
- **Locked in** (net < -2): Restraining forces dominate — candidate unlikely to switch without a major trigger event

**Identify switching catalysts:**
- Trigger events that could tip the balance (contract renewal, team change, compliance deadline, competitive loss)
- Anxiety reducers that could lower barriers (free trial, migration assistance, case studies, gradual rollout)
- Habit breakers that could disrupt inertia (team turnover, platform deprecation, process audit, leadership change)

### 7. Validate with User

Present force maps, scores, balance analysis, and switching catalyst recommendations. Ask for corrections on:
- Force completeness: missing push/pull/anxiety/habit factors
- Intensity accuracy: whether scores match known reality
- Evidence grounding: whether factors are based on real signals or assumptions
- Catalyst plausibility: whether identified triggers are realistic

## Output

### `research/customer-discovery-four-forces.md` (or `research/{slug}/customer-discovery-four-forces.md`)

```markdown
# Four Forces of Progress Analysis

> Based on: [sources]
> Date: [current date]
> Methodology: Moesta Four Forces of Progress (Push/Pull/Anxiety/Habit)

## ICP Candidate: [Name]

### Push Forces (Current Pain)
| Factor | Category | Intensity | Frequency | Evidence | Source |
|--------|----------|-----------|-----------|----------|--------|
| [pain point] | Functional/Financial/Emotional/Social | 1-10 | daily/weekly/monthly | Observed/Inferred/Hypothesized | [source] |

### Pull Forces (New Solution Attraction)
| Factor | Category | Intensity | Specificity | Evidence | Source |
|--------|----------|-----------|-------------|----------|--------|
| [attraction] | Functional/Financial/Emotional/Social | 1-10 | Generic/Concrete | Observed/Inferred/Hypothesized | [source] |

### Anxiety Forces (Fear of Change)
| Factor | Category | Intensity | Addressability | Evidence | Source |
|--------|----------|-----------|----------------|----------|--------|
| [concern] | Performance/Implementation/Financial/Social | 1-10 | Easy/Moderate/Hard | Observed/Inferred/Hypothesized | [source] |

### Habit Forces (Status Quo Inertia)
| Factor | Category | Intensity | Disruption Cost | Evidence | Source |
|--------|----------|-----------|-----------------|----------|--------|
| [habit] | Behavioral/Organizational/Emotional/Switching Cost | 1-10 | Low/Medium/High | Observed/Inferred/Hypothesized | [source] |

### Force Balance
| Metric | Score |
|--------|-------|
| Total Push | [sum] |
| Total Pull | [sum] |
| Total Anxiety | [sum] |
| Total Habit | [sum] |
| Driving Forces (Push + Pull) | [sum] |
| Restraining Forces (Anxiety + Habit) | [sum] |
| Net Switching Momentum | [driving - restraining] |
| Classification | Strong/Moderate/Stalled/Locked-in |

### Switching Catalysts
- **Trigger events**: [events that could tip the balance]
- **Anxiety reducers**: [actions to lower barriers]
- **Habit breakers**: [disruptions to status quo inertia]

## ICP Candidate: [Name 2]
...

## Cross-Candidate Force Comparison
| Candidate | Push | Pull | Anxiety | Habit | Net Momentum | Classification |
|-----------|------|------|---------|-------|--------------|----------------|
| [name] | [sum] | [sum] | [sum] | [sum] | [net] | [class] |

## Dominant Force Patterns
### Strongest Push Factors (across candidates)
1. [factor] — avg intensity [score], affects [N] candidates
2. [factor] — avg intensity [score], affects [N] candidates

### Strongest Pull Factors (across candidates)
1. [factor] — avg intensity [score], affects [N] candidates

### Highest Anxiety Factors (across candidates)
1. [factor] — avg intensity [score], affects [N] candidates

### Strongest Habit Factors (across candidates)
1. [factor] — avg intensity [score], affects [N] candidates

## Strategic Implications
- **Messaging priority**: Lead with [push/pull] because [reason]
- **Objection handling**: Address [top anxiety factors] via [approach]
- **Onboarding focus**: Break [top habit factors] by [approach]
- **Timing strategy**: Watch for [trigger events] as switching catalysts

## Evidence Matrix
| Claim | Evidence Source | Evidence Type | Confidence |
|-------|---------------|---------------|------------|
| [claim] | [source] | Observed/Inferred/Hypothesized | High/Medium/Low |
```

## Constraints

- Ground every force, score, and catalyst in evidence from ICP candidates, research, specs, feedback, or codebase.
- Use Moesta's Four Forces framework faithfully — do not collapse forces into generic pros/cons.
- Score intensity honestly; do not inflate push/pull or deflate anxiety/habit to bias toward switching.
- Do not prescribe UI or architecture — describe the switching dynamics, not the solution.
- Present findings before writing.
- Do not overwrite existing output without asking the user first.
- This is a child framework skill in the `customer-discovery` Research Session Loop. Do not emit cross-skill or downstream routing from framework stops, and do not recommend execution-loop commands or path-shaped child framework invocations. Inline framework handoff sections must name only the parent command `$customer-discovery`.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/four-forces-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
