---
name: seven-dimensions
description: Lincoln Murphy 7 Dimensions of ICP — score ICP candidates on Readiness, Willingness, Ability, Success Potential, Acquisition Efficiency, Ascension Potential, and Advocacy Potential for composite fitness scoring
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: customer-discovery
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# 7 Dimensions of ICP — Lincoln Murphy Ideal Customer Profile Scoring

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
  framework_slug: seven-dimensions
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

### 2. Dimension 1 — Readiness

For each ICP candidate, assess technical and operational readiness to adopt the solution:

**Infrastructure readiness** — existing technical foundation:
- Current technology stack compatibility (APIs, platforms, data formats)
- Infrastructure maturity (cloud adoption, automation level, monitoring)
- Data readiness (quality, accessibility, integration points)
- Security and compliance posture (certifications, policies, review processes)

**Team readiness** — people and skills in place:
- Relevant technical expertise on staff (or accessible via partners)
- Dedicated personnel who would own implementation and ongoing use
- Cross-functional alignment between technical and business teams
- Previous experience adopting similar tools or solutions

**Process readiness** — operational maturity to absorb change:
- Defined workflows that the solution would plug into or improve
- Change management processes for introducing new tools
- Measurement and feedback loops already in place
- Governance structures that support adoption decisions

Score: **Readiness** (1-5: 1=no foundation, 2=early stage, 3=partially ready, 4=mostly ready, 5=fully ready), **Evidence strength** (Observed/Inferred/Hypothesized).

### 3. Dimension 2 — Willingness

For each ICP candidate, assess cultural and organizational willingness to change:

**Cultural openness** — attitude toward new approaches:
- Organizational culture around innovation and experimentation
- History of adopting new tools or processes (early adopter vs. laggard)
- Tolerance for the learning curve and temporary productivity dips
- Leadership messaging about modernization or transformation

**Urgency and motivation** — internal pressure to act:
- Recognized pain from the status quo (not just latent dissatisfaction)
- Executive or leadership sponsorship for the category of solution
- Competitive pressure creating urgency to change
- Strategic initiatives that align with adoption

**Champion presence** — internal advocates:
- Identifiable champion(s) with authority and motivation to push adoption
- Champion's organizational influence and political capital
- Track record of the champion driving similar changes
- Breadth of support (single champion vs. coalition)

Score: **Willingness** (1-5: 1=resistant, 2=skeptical, 3=open, 4=eager, 5=actively seeking), **Evidence strength** (Observed/Inferred/Hypothesized).

### 4. Dimension 3 — Ability

For each ICP candidate, assess financial and resource ability to invest:

**Budget capacity** — financial resources available:
- Budget allocated or allocable for this category of solution
- Budget authority level required and likelihood of approval
- Competing budget priorities and funding cycles
- Price sensitivity and willingness to pay at the solution's price point

**Resource capacity** — people and time available:
- Headcount available for implementation and ongoing use
- Timeline capacity (not over-committed on competing projects)
- Access to external resources (consultants, integrators) if needed
- Organizational bandwidth for change alongside day-to-day operations

**Decision capacity** — ability to make and execute purchase decisions:
- Procurement process complexity and typical cycle length
- Number of stakeholders required for approval
- Legal and compliance review requirements
- Vendor evaluation and onboarding process maturity

Score: **Ability** (1-5: 1=unable, 2=constrained, 3=feasible, 4=comfortable, 5=well-resourced), **Evidence strength** (Observed/Inferred/Hypothesized).

### 5. Dimension 4 — Success Potential

For each ICP candidate, assess likelihood of achieving meaningful outcomes:

**Use-case fit** — alignment between need and solution:
- How well the solution addresses the candidate's primary pain points
- Gap severity between current state and desired state
- Fit with the candidate's specific workflow and context
- Edge cases or requirements the solution may not cover

**Success criteria alignment** — shared definition of success:
- Clarity of the candidate's success metrics and expectations
- Alignment between what the solution delivers and what the candidate measures
- Realistic timeline expectations for achieving outcomes
- Historical precedent for similar solutions delivering in this context

**Outcome achievability** — practical path to results:
- Complexity of implementation relative to the candidate's capacity
- Dependencies on external factors (integrations, data quality, behavior change)
- Risk factors that could prevent full value realization
- Support and enablement needed to reach meaningful outcomes

Score: **Success Potential** (1-5: 1=unlikely, 2=challenging, 3=moderate, 4=strong, 5=near-certain), **Evidence strength** (Observed/Inferred/Hypothesized).

### 6. Dimension 5 — Acquisition Efficiency

For each ICP candidate, assess the cost and effort to acquire them as a customer:

**Channel accessibility** — how easily you can reach them:
- Presence in your existing marketing and sales channels
- Responsiveness to outbound or inbound engagement
- Community and network overlap with your existing customer base
- Content and messaging resonance with this candidate's context

**Sales cycle dynamics** — complexity of the buying process:
- Expected length of sales cycle (days to months)
- Number of stakeholders and decision-makers involved
- Technical evaluation or proof-of-concept requirements
- Procurement and legal review overhead

**Competitive displacement** — effort to win against alternatives:
- Current solution (incumbent, manual process, or nothing)
- Switching costs and lock-in with existing solutions
- Competitive intensity in this segment
- Differentiation strength against likely alternatives

Score: **Acquisition Efficiency** (1-5: 1=very expensive, 2=costly, 3=moderate, 4=efficient, 5=highly efficient), **Evidence strength** (Observed/Inferred/Hypothesized).

### 7. Dimension 6 — Ascension Potential

For each ICP candidate, assess likelihood of expanding over time:

**Upsell and cross-sell paths** — product expansion opportunity:
- Additional features, tiers, or modules the candidate would likely need
- Natural progression from initial use case to broader adoption
- Price point growth potential as value is demonstrated
- Add-on or premium capability alignment with candidate needs

**Organizational growth trajectory** — expanding footprint:
- Candidate's growth rate and trajectory (headcount, revenue, usage)
- Multi-team or multi-department expansion potential
- Geographic or market expansion that drives additional need
- Platform or ecosystem stickiness that deepens over time

**Usage deepening** — increasing engagement over time:
- Likelihood of increasing usage intensity within initial scope
- Potential for the solution to become workflow-critical
- Network effects or viral adoption within the organization
- Integration depth that increases dependency and value

Score: **Ascension Potential** (1-5: 1=flat, 2=limited, 3=moderate, 4=strong, 5=high-growth), **Evidence strength** (Observed/Inferred/Hypothesized).

### 8. Dimension 7 — Advocacy Potential

For each ICP candidate, assess likelihood of becoming a referral source:

**Brand alignment** — fit between your brand and theirs:
- Prestige or recognition value of having them as a customer
- Alignment between their brand values and your positioning
- Logo or case study value for your target market
- Industry influence that lends credibility to your solution

**Community activity** — propensity to share and recommend:
- Active participation in industry communities, conferences, or forums
- History of writing, speaking, or sharing about tools they use
- Social media presence and engagement in relevant channels
- Willingness to participate in case studies, reviews, or testimonials

**Network influence** — reach and quality of referral potential:
- Size and relevance of professional network in your target market
- Influence on peers' technology and process decisions
- Connections to other high-value potential customers
- Position as a thought leader or trusted advisor in their space

Score: **Advocacy Potential** (1-5: 1=unlikely, 2=passive, 3=willing, 4=active, 5=evangelist), **Evidence strength** (Observed/Inferred/Hypothesized).

### 9. ICP Fitness Synthesis

Cross-dimension analysis to surface composite ICP fitness and strategic patterns:

**Composite fitness scoring:**
- Calculate weighted composite score per ICP candidate across all 7 dimensions
- Identify dimension clusters (e.g., Ready+Willing+Able as "adoption readiness", Success+Acquisition as "value efficiency", Ascension+Advocacy as "growth multiplier")
- Flag candidates with high composite scores but critical dimension gaps

**Dimension gap analysis:**
- Map which dimensions are strong vs. weak per candidate
- Identify dimensions where gaps are addressable (e.g., Readiness gaps can be solved with onboarding) vs. structural (e.g., low Willingness may be cultural)
- Prioritize gap-closing investments by ROI: which dimension improvements unlock the most composite score improvement

**Cross-candidate comparison:**
- Rank candidates by composite fitness score
- Identify candidate archetypes (e.g., "ready but won't grow" vs. "high-growth but hard to acquire")
- Surface trade-offs between candidates optimized for different business objectives (revenue now vs. growth later vs. brand building)

**Strategic implications:**
- ICP prioritization recommendations based on composite fitness
- Go-to-market focus: which dimensions to lead with in positioning and sales
- Product and enablement priorities: which dimension gaps the product or onboarding should address
- Portfolio balance: recommended mix of candidate types for sustainable growth

### 10. Validate with User

Present dimension analyses, composite fitness scoring, and cross-candidate comparison. Ask for corrections on:
- Dimension completeness: missing evidence or considerations in any of the seven dimensions
- Scoring accuracy: whether dimension scores match known reality for each candidate
- Evidence grounding: whether assessments are based on real evidence or assumptions
- Strategic alignment: whether the prioritization recommendations match business objectives

## Output

### `research/customer-discovery-seven-dimensions.md` (or `research/{slug}/customer-discovery-seven-dimensions.md`)

```markdown
# 7 Dimensions of ICP Analysis

> Based on: [sources]
> Date: [current date]
> Methodology: Lincoln Murphy 7 Dimensions of ICP (Readiness, Willingness, Ability, Success Potential, Acquisition Efficiency, Ascension Potential, Advocacy Potential)

## ICP Candidate: [Name]

### Dimension 1: Readiness
| Factor | Category | Score (1-5) | Evidence | Source |
|--------|----------|-------------|----------|--------|
| [factor] | Infrastructure/Team/Process | 1-5 | Observed/Inferred/Hypothesized | [source] |

### Dimension 2: Willingness
| Factor | Category | Score (1-5) | Evidence | Source |
|--------|----------|-------------|----------|--------|
| [factor] | Cultural Openness/Urgency/Champion | 1-5 | Observed/Inferred/Hypothesized | [source] |

### Dimension 3: Ability
| Factor | Category | Score (1-5) | Evidence | Source |
|--------|----------|-------------|----------|--------|
| [factor] | Budget/Resource/Decision Capacity | 1-5 | Observed/Inferred/Hypothesized | [source] |

### Dimension 4: Success Potential
| Factor | Category | Score (1-5) | Evidence | Source |
|--------|----------|-------------|----------|--------|
| [factor] | Use-Case Fit/Criteria Alignment/Achievability | 1-5 | Observed/Inferred/Hypothesized | [source] |

### Dimension 5: Acquisition Efficiency
| Factor | Category | Score (1-5) | Evidence | Source |
|--------|----------|-------------|----------|--------|
| [factor] | Channel Access/Sales Cycle/Competitive Displacement | 1-5 | Observed/Inferred/Hypothesized | [source] |

### Dimension 6: Ascension Potential
| Factor | Category | Score (1-5) | Evidence | Source |
|--------|----------|-------------|----------|--------|
| [factor] | Upsell Paths/Org Growth/Usage Deepening | 1-5 | Observed/Inferred/Hypothesized | [source] |

### Dimension 7: Advocacy Potential
| Factor | Category | Score (1-5) | Evidence | Source |
|--------|----------|-------------|----------|--------|
| [factor] | Brand Alignment/Community Activity/Network Influence | 1-5 | Observed/Inferred/Hypothesized | [source] |

### Dimension Coverage
| Dimension | Score | Depth | Key Gaps | Confidence |
|-----------|-------|-------|----------|------------|
| Readiness | 1-5 | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Willingness | 1-5 | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Ability | 1-5 | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Success Potential | 1-5 | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Acquisition Efficiency | 1-5 | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Ascension Potential | 1-5 | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |
| Advocacy Potential | 1-5 | Deep/Moderate/Shallow | [gaps] | High/Medium/Low |

## ICP Candidate: [Name 2]
...

## Cross-Candidate Composite Fitness Comparison
| Candidate | Readiness | Willingness | Ability | Success | Acquisition | Ascension | Advocacy | Composite | Archetype |
|-----------|-----------|-------------|---------|---------|-------------|-----------|----------|-----------|-----------|
| [name] | 1-5 | 1-5 | 1-5 | 1-5 | 1-5 | 1-5 | 1-5 | [weighted] | [type] |

## Dimension Cluster Analysis
### Adoption Readiness (Ready + Willing + Able)
- [cluster patterns and implications]

### Value Efficiency (Success + Acquisition)
- [cluster patterns and implications]

### Growth Multiplier (Ascension + Advocacy)
- [cluster patterns and implications]

## Dimension Gap Analysis
| Candidate | Weakest Dimension | Gap Type | Addressability | Recommended Action |
|-----------|------------------|----------|----------------|-------------------|
| [name] | [dimension] | Structural/Addressable | Easy/Moderate/Difficult | [action] |

## Strategic Implications
- **ICP prioritization**: Focus on [candidates] because [reason]
- **Go-to-market focus**: Lead with [dimensions] because [reason]
- **Product priorities**: Address [dimension gaps] to unlock [outcome]
- **Portfolio balance**: Mix [candidate types] for [growth strategy]

## Evidence Matrix
| Claim | Evidence Source | Evidence Type | Confidence |
|-------|---------------|---------------|------------|
| [claim] | [source] | Observed/Inferred/Hypothesized | High/Medium/Low |
```

## Constraints

- Ground every assessment, score, and recommendation in evidence from ICP candidates, research, specs, feedback, or codebase.
- Use Lincoln Murphy's 7 Dimensions framework faithfully — do not collapse dimensions into generic ICP analysis.
- Score each dimension honestly; do not inflate scores to present a false sense of ICP fitness.
- Do not prescribe UI or architecture — describe ICP fitness characteristics, not the solution.
- Present findings before writing.
- Do not overwrite existing output without asking the user first.
- This is a child framework skill in the `customer-discovery` Research Session Loop. Do not emit cross-skill or downstream routing from framework stops, and do not recommend execution-loop commands or path-shaped child framework invocations. Inline framework handoff sections must name only the parent command `$customer-discovery`.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/seven-dimensions-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
