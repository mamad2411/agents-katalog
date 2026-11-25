---
name: five-rings
description: Revella Five Rings of Buying Insight — map Priority Initiatives, Success Factors, Perceived Barriers, Decision Criteria, and Buyer's Journey per ICP candidate to understand B2B buyer decision psychology
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: customer-discovery
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Five Rings of Buying Insight — Revella Buyer Decision Analysis

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
  framework_slug: five-rings
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

### 2. Ring 1 — Priority Initiatives

For each ICP candidate, identify what triggers the buying process — the circumstances that cause a buyer to allocate time, budget, and political capital to solving this problem now:

**Trigger events** — what changed in their world:
- Organizational changes (new leadership, restructuring, mergers, growth milestones)
- Market shifts (competitive pressure, regulatory changes, industry trends)
- Technical catalysts (system failures, end-of-life announcements, scalability limits)
- Financial triggers (budget cycles, cost overruns, new funding, revenue pressure)

**Urgency drivers** — why this problem demands attention now:
- Deadlines or time-bound obligations (compliance dates, contract renewals, launch windows)
- Escalating consequences of inaction (growing costs, accumulating risk, widening gaps)
- Opportunity windows that will close (market timing, competitive advantage, early-mover benefit)
- Internal momentum (executive sponsorship, team readiness, aligned initiatives)

**Investment willingness signals** — evidence they will commit resources:
- Budget already allocated or being requested
- Stakeholders actively championing the initiative
- RFP or formal evaluation process underway
- Existing workarounds consuming enough resources to justify investment

Score each initiative: **Urgency** (1-5: latent/aware/exploring/committed/urgent), **Investment readiness** (Low/Medium/High), **Evidence strength** (Observed/Inferred/Hypothesized).

### 3. Ring 2 — Success Factors

For each ICP candidate, identify the outcomes buyers expect — what "success" looks like from their perspective after adopting a solution:

**Operational outcomes** — measurable improvements to daily work:
- Time savings on specific workflows or tasks
- Error reduction or quality improvements
- Throughput or capacity increases
- Process simplification or automation gains

**Business outcomes** — impact on organizational goals:
- Revenue growth or protection
- Cost reduction or resource optimization
- Risk mitigation or compliance achievement
- Competitive advantage or market position improvement

**Personal outcomes** — what success means for the individual buyer:
- Career advancement or visibility from a successful initiative
- Reduced stress or cognitive load
- Professional development or skill growth
- Reputation as an innovator or effective leader

**Team outcomes** — impact on the buyer's team and collaborators:
- Improved team productivity or morale
- Better cross-functional collaboration
- Reduced friction with upstream/downstream teams
- Enhanced ability to attract and retain talent

Score each success factor: **Priority** (must-have/important/nice-to-have), **Measurability** (quantifiable/observable/subjective), **Evidence strength** (Observed/Inferred/Hypothesized).

### 4. Ring 3 — Perceived Barriers

For each ICP candidate, identify the concerns that make buyers hesitate — real or perceived obstacles that slow or stop the buying process:

**Technical barriers** — concerns about capability and fit:
- Fear that the solution won't handle their specific use cases or edge cases
- Concern about integration complexity with existing systems
- Worry about data migration risks and fidelity
- Skepticism about performance claims or scalability

**Organizational barriers** — internal resistance and process friction:
- Difficulty getting stakeholder alignment or budget approval
- Resistance from teams who must change their workflows
- Competing priorities that crowd out this initiative
- Previous failed implementations that create institutional skepticism

**Vendor/solution barriers** — concerns about the provider:
- Worry about vendor viability, longevity, or commitment
- Concern about lock-in or switching costs if the solution doesn't work out
- Skepticism about support quality or responsiveness
- Unease about pricing transparency or total cost of ownership

**Knowledge barriers** — gaps in understanding that create friction:
- Lack of clarity about what the solution actually does vs. marketing claims
- Difficulty evaluating alternatives without domain expertise
- Uncertainty about implementation timeline and effort required
- Missing proof points or reference cases from similar organizations

Score each barrier: **Severity** (blocking/significant/minor), **Addressability** (easy to resolve/requires effort/deeply entrenched), **Evidence strength** (Observed/Inferred/Hypothesized).

### 5. Ring 4 — Decision Criteria

For each ICP candidate, identify how buyers compare and choose between alternatives — the specific attributes, features, and requirements they use to evaluate options:

**Functional criteria** — what the solution must do:
- Required capabilities and features (table-stakes vs. differentiators)
- Performance thresholds (speed, accuracy, reliability, uptime)
- Integration requirements (APIs, data formats, platform compatibility)
- Customization and extensibility needs

**Relationship criteria** — who they want to work with:
- Vendor reputation, track record, and industry presence
- Quality of sales, onboarding, and support experience
- Cultural fit and communication style
- Community, ecosystem, and partner network

**Economic criteria** — what it must cost:
- Pricing model preferences (subscription, usage-based, perpetual, freemium)
- Total cost of ownership expectations (implementation, training, maintenance)
- ROI timeline expectations and payback period
- Budget constraints and approval thresholds

**Risk criteria** — what they need to feel safe:
- Security, compliance, and data governance requirements
- Contract flexibility (terms, exit clauses, SLAs)
- Reference customers in their industry or scale
- Proof of concept or trial availability

Score each criterion: **Weight** (critical/important/tiebreaker), **Consensus** (all stakeholders agree/some disagree/contested), **Evidence strength** (Observed/Inferred/Hypothesized).

### 6. Ring 5 — Buyer's Journey

For each ICP candidate, map the process from trigger to decision — who is involved, what they do at each stage, and where the process stalls or accelerates:

**Awareness stage** — how they discover and frame the problem:
- How the buyer first recognizes the problem or opportunity
- What research they do before engaging vendors (search, peers, analysts, communities)
- Who they consult internally to validate the need
- How they frame the problem (symptoms vs. root cause, scope, urgency)

**Consideration stage** — how they explore and evaluate options:
- How they build their initial consideration set (referrals, search, analyst reports, events)
- What content and proof points they consume during evaluation
- How they narrow from long list to short list
- What internal process they follow (formal RFP, informal evaluation, committee review)

**Decision stage** — how they choose and commit:
- Who has final decision authority and who influences the decision
- How the buying committee is structured (champion, influencer, blocker, decision-maker, end-user)
- What final validation they need before committing (POC, reference calls, security review, legal review)
- Common stall points and what unblocks them

**Post-decision stage** — what happens after the decision:
- How they justify the purchase internally
- What their onboarding and rollout expectations are
- How they measure early success or failure
- What would trigger them to reconsider or expand

Map the journey timeline: **Typical duration** (trigger to decision), **Key milestones**, **Common stall points**, **Evidence strength** (Observed/Inferred/Hypothesized).

### 7. Buying Insight Synthesis

Cross-ring analysis to surface strategic patterns:

**Insight coverage matrix:**
- Map which rings have strong evidence vs. gaps per ICP candidate
- Identify rings where insight depth is shallow and flag for further research

**Cross-ring connections:**
- How Priority Initiatives shape Success Factors (what they need because of why they're buying)
- How Perceived Barriers relate to Decision Criteria (barriers that become evaluation filters)
- How the Buyer's Journey reveals when each ring's insights matter most

**Buyer persona correlation:**
- Which insights cluster by buyer role (champion, influencer, decision-maker, end-user)
- Where buyer roles diverge on success factors, barriers, or decision criteria
- Key personas whose barriers or criteria are under-represented in the evidence

**Strategic implications:**
- Messaging priorities per ring and buyer persona
- Content and proof point gaps that map to buyer journey stages
- Competitive positioning opportunities based on decision criteria
- Sales process recommendations based on journey mapping

### 8. Validate with User

Present ring analyses, insight synthesis, and buyer persona correlations. Ask for corrections on:
- Ring completeness: missing insights in any of the five rings
- Scoring accuracy: whether urgency, priority, severity, weight, and timeline scores match known reality
- Evidence grounding: whether insights are based on real buyer evidence or assumptions
- Persona accuracy: whether buyer role correlations reflect actual buying dynamics

## Output

### `research/customer-discovery-five-rings.md` (or `research/{slug}/customer-discovery-five-rings.md`)

```markdown
# Five Rings of Buying Insight Analysis

> Based on: [sources]
> Date: [current date]
> Methodology: Revella Five Rings of Buying Insight (Priority Initiatives, Success Factors, Perceived Barriers, Decision Criteria, Buyer's Journey)

## ICP Candidate: [Name]

### Ring 1: Priority Initiatives
| Initiative | Trigger Type | Urgency | Investment Readiness | Evidence | Source |
|------------|-------------|---------|---------------------|----------|--------|
| [initiative] | Event/Market/Technical/Financial | 1-5 | Low/Medium/High | Observed/Inferred/Hypothesized | [source] |

### Ring 2: Success Factors
| Success Factor | Category | Priority | Measurability | Evidence | Source |
|---------------|----------|----------|---------------|----------|--------|
| [outcome] | Operational/Business/Personal/Team | Must-have/Important/Nice-to-have | Quantifiable/Observable/Subjective | Observed/Inferred/Hypothesized | [source] |

### Ring 3: Perceived Barriers
| Barrier | Category | Severity | Addressability | Evidence | Source |
|---------|----------|----------|----------------|----------|--------|
| [concern] | Technical/Organizational/Vendor/Knowledge | Blocking/Significant/Minor | Easy/Effort/Entrenched | Observed/Inferred/Hypothesized | [source] |

### Ring 4: Decision Criteria
| Criterion | Category | Weight | Consensus | Evidence | Source |
|-----------|----------|--------|-----------|----------|--------|
| [criterion] | Functional/Relationship/Economic/Risk | Critical/Important/Tiebreaker | All agree/Some disagree/Contested | Observed/Inferred/Hypothesized | [source] |

### Ring 5: Buyer's Journey
| Stage | Key Activities | Key Players | Duration | Stall Points | Evidence |
|-------|---------------|-------------|----------|--------------|----------|
| Awareness | [activities] | [roles] | [time] | [stalls] | Observed/Inferred/Hypothesized |
| Consideration | [activities] | [roles] | [time] | [stalls] | Observed/Inferred/Hypothesized |
| Decision | [activities] | [roles] | [time] | [stalls] | Observed/Inferred/Hypothesized |
| Post-decision | [activities] | [roles] | [time] | [stalls] | Observed/Inferred/Hypothesized |

### Insight Coverage
| Ring | Depth | Key Gaps | Confidence |
|------|-------|----------|------------|
| Priority Initiatives | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Success Factors | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Perceived Barriers | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Decision Criteria | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Buyer's Journey | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |

## ICP Candidate: [Name 2]
...

## Cross-Candidate Buying Insight Comparison
| Candidate | Top Initiative | Top Success Factor | Top Barrier | Top Criterion | Journey Duration | Overall Depth |
|-----------|---------------|-------------------|-------------|--------------|-----------------|---------------|
| [name] | [initiative] | [factor] | [barrier] | [criterion] | [duration] | Deep/Moderate/Shallow |

## Buyer Persona Correlation
| Insight | Champion | Influencer | Decision-Maker | End-User | Blocker |
|---------|----------|-----------|----------------|----------|---------|
| [insight from any ring] | [relevance] | [relevance] | [relevance] | [relevance] | [relevance] |

## Cross-Ring Patterns
### Priority Initiatives → Success Factors
- [how trigger X shapes expected outcome Y]

### Perceived Barriers → Decision Criteria
- [how concern X becomes evaluation filter Y]

### Buyer's Journey Stage → Ring Relevance
- [which insights matter at which journey stage]

## Strategic Implications
- **Messaging priority**: Lead with [ring/insight] because [reason]
- **Content strategy**: Address [journey stage] gaps with [content type]
- **Objection handling**: Counter [top barriers] via [approach]
- **Sales process**: Align to [buyer's journey] by [approach]
- **Competitive positioning**: Differentiate on [decision criteria] because [reason]

## Evidence Matrix
| Claim | Evidence Source | Evidence Type | Confidence |
|-------|---------------|---------------|------------|
| [claim] | [source] | Observed/Inferred/Hypothesized | High/Medium/Low |
```

## Constraints

- Ground every insight, score, and recommendation in evidence from ICP candidates, research, specs, feedback, or codebase.
- Use Revella's Five Rings framework faithfully — do not collapse rings into generic buyer analysis.
- Score depth and coverage honestly; do not inflate insight confidence to present a false sense of completeness.
- Do not prescribe UI or architecture — describe buyer decision psychology, not the solution.
- Present findings before writing.
- Do not overwrite existing output without asking the user first.
- This is a child framework skill in the `customer-discovery` Research Session Loop. Do not emit cross-skill or downstream routing from framework stops, and do not recommend execution-loop commands or path-shaped child framework invocations. Inline framework handoff sections must name only the parent command `$customer-discovery`.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/five-rings-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
