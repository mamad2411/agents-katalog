---
name: pmf-engine
description: Vohra/Supan PMF Engine - evaluate existing user data with Sean Ellis PMF signal, very-disappointed segmentation, retention/usage evidence, and High-Expectation Customer synthesis
type: research
version: v0.9
required_conventions: [alignment-page]
invocation: sub-skill
parent: customer-discovery
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# PMF Engine - Vohra/Supan Product-Market Fit Analysis

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
  framework_slug: pmf-engine
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
- **Hard**: Real user or customer evidence must exist. Acceptable evidence includes `research/customer-feedback.md`, survey/interview data, support tickets, churn/retention notes, product analytics, sales calls, usage logs, or a user-provided dataset. If no real-user evidence exists, explain that PMF Engine is unavailable for pre-product work and stop.
- **Soft**: `research/competitive-analysis.md`, specs, product analytics exports, NPS/CSAT reports, cohort retention data, customer support records, sales notes, and codebase context when available.

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

### 1. Load Context And Evidence

- Read ICP candidates from orchestrator working packet (`research/_working/preliminary-customer-discovery-research.md`) or `research/icp.md`.
- Read real-user evidence: `research/customer-feedback.md`, survey results, interview notes, support tickets, sales notes, churn notes, retention/cohort reports, product analytics, usage logs, or user-provided datasets.
- Read idea brief, competitive analysis, specs, README, CLAUDE.md, and codebase context when available.
- Classify evidence by source type, recency, sample size, segment coverage, and bias risk.
- Separate actual observed user/customer data from founder hypotheses, analyst inference, and marketing claims.

### 2. Data Readiness And PMF Survey Coverage

Assess whether the evidence can support the Vohra/Superhuman PMF Engine and HXC synthesis:

**PMF survey availability**
- Whether the Sean Ellis question is present: "How would you feel if you could no longer use this product?"
- Response distribution across Very disappointed, Somewhat disappointed, Not disappointed, and N/A.
- Sample size, response bias, segment coverage, and whether respondents are active users.
- Whether supporting questions exist: who would benefit most, main benefit received, alternatives used, and desired improvements.

**Behavioral evidence availability**
- Retention, activation, frequency, depth of use, expansion, repeat purchase, or renewal data.
- Qualitative evidence from interviews, support, churn reasons, sales calls, and onboarding notes.
- Segment-level differences between high-love users and lukewarm or churned users.

**Data-readiness verdict**
- Classify as Strong / Partial / Insufficient.
- If insufficient, identify the minimum evidence needed before PMF Engine can produce a reliable verdict.

### 3. Sean Ellis PMF Signal

When survey data exists, calculate and interpret PMF signal:

**Very-disappointed threshold**
- Calculate the percentage of respondents who would be Very disappointed.
- Treat 40%+ as a positive PMF signal, but do not treat it as sufficient by itself.
- Segment the signal by ICP candidate, role, company type, use case, acquisition source, tenure, and engagement where evidence allows.

**Signal quality**
- Check whether respondents are representative of the target user base.
- Identify inflated signal risks: tiny sample size, only enthusiasts responding, founder-picked respondents, inactive-user exclusion, or ambiguous product definition.
- Identify hidden weak spots: users love one workflow but reject the broader product, decision-makers differ from daily users, or retention contradicts survey love.

### 4. Very-Disappointed Segment Analysis

Analyze the "very disappointed" cohort to identify who gets irreplaceable value:

**Segment attributes**
- Role, company type, size, maturity, workflow, urgency, technical readiness, buying context, and product use case.
- Acquisition path and activation path.
- Retention, expansion, support burden, and engagement patterns.

**Loved benefit**
- The specific outcome, workflow, or emotional relief that makes the product hard to lose.
- User language for the benefit, not only agent summaries.
- Differences between what users say they value and what their behavior indicates.

**Alternatives and switching**
- What users would do without the product.
- Which alternatives are inadequate and why.
- Whether users are switching from nothing, manual workarounds, an incumbent tool, or another team member's labor.

### 5. High-Expectation Customer Synthesis

Synthesize the High-Expectation Customer (HXC): the most discerning customer within the target market who still gets exceptional value.

**HXC profile**
- Who they are, what they are trying to accomplish, and why their expectations are high.
- What makes them hard to satisfy and why the product still works for them.
- What they refuse to tolerate: workflow friction, missing integrations, quality gaps, risk, pricing friction, or trust issues.

**HXC value wedge**
- The narrow product promise that this customer would miss most.
- Why the promise is meaningfully better than alternatives for this segment.
- Which product qualities must remain non-negotiable to keep the HXC.

**Exclusion logic**
- Adjacent users or buyers who look attractive but do not fit the HXC.
- Segments with high willingness but poor retention, high usage but no budget, or strong pain but no realistic success path.

### 6. Target Segment And Product Focus

Use PMF signal and HXC synthesis to narrow ICP recommendations:

**Primary segment**
- Recommend the segment with the strongest combination of PMF signal, behavioral evidence, HXC fit, and business viability.
- Explain whether the segment is ready for positioning, requires more validation, or should remain provisional.

**Product focus**
- Identify the features, workflows, or promises to double down on for the target segment.
- Identify requests to ignore, defer, or treat as segment-specific because they dilute the loved benefit.
- Identify onboarding, activation, or messaging changes that could increase very-disappointed share.

**Risks**
- Retention contradiction, buyer/user mismatch, sample-size weakness, insufficient product maturity, low willingness to pay, or overfitting to a small enthusiastic group.

### 7. Validate With User

Present PMF signal, very-disappointed segment analysis, HXC synthesis, and target-segment recommendation. Ask for corrections on:
- Evidence completeness: missing surveys, interviews, analytics, churn notes, or support records.
- Segment accuracy: whether the high-love segment matches known users and buyers.
- HXC realism: whether the proposed HXC is demanding enough and still reachable.
- Product focus: whether the recommended double-downs and exclusions match known product strategy.

## Output

### `research/customer-discovery-pmf-engine.md` (or `research/{slug}/customer-discovery-pmf-engine.md`)

```markdown
# PMF Engine Analysis

> Based on: [sources]
> Date: [current date]
> Methodology: Vohra/Supan PMF Engine (Sean Ellis PMF signal, Very-Disappointed segmentation, High-Expectation Customer synthesis)

## Data Readiness
| Evidence Type | Available? | Sample / Coverage | Bias Risk | Notes |
|---------------|------------|-------------------|-----------|-------|
| PMF survey | Yes/No/Partial | [count/segments] | Low/Medium/High | [notes] |
| Behavioral usage | Yes/No/Partial | [coverage] | Low/Medium/High | [notes] |
| Retention/churn | Yes/No/Partial | [coverage] | Low/Medium/High | [notes] |
| Customer interviews/support | Yes/No/Partial | [coverage] | Low/Medium/High | [notes] |

## PMF Signal
| Segment | Very Disappointed % | Sample Size | Supportive Behavioral Evidence | Confidence |
|---------|---------------------|-------------|--------------------------------|------------|
| [segment] | [percent] | [n] | [retention/usage/renewal] | High/Medium/Low |

## Very-Disappointed Segment
### Segment Attributes
- [role/company/use case/maturity/acquisition path]

### Loved Benefit
- [user-language description of the benefit users would miss]

### Alternatives
| Alternative | Why Users Would Switch There | Why It Falls Short | Evidence |
|-------------|------------------------------|--------------------|----------|
| [alternative] | [reason] | [gap] | [source] |

## High-Expectation Customer
### HXC Profile
- **Customer**: [specific profile]
- **High expectations**: [what makes them demanding]
- **Why this product works**: [evidence-backed reason]
- **Non-negotiables**: [quality/workflow/trust requirements]

### HXC Value Wedge
- [narrow promise and why it is better than alternatives]

### Exclusions
| Excluded Segment | Why It Looks Attractive | Why It Is Not HXC | Evidence |
|------------------|-------------------------|-------------------|----------|
| [segment] | [signal] | [fit issue] | [source] |

## Target Segment Recommendation
- **Primary target**: [segment]
- **Verdict**: Strong PMF signal / partial signal / insufficient evidence
- **Reasoning**: [evidence-backed rationale]
- **Product focus**: [double-downs]
- **Defer or ignore**: [requests/segments/features that dilute focus]

## Evidence Matrix
| Claim | Evidence Source | Evidence Type | Confidence |
|-------|-----------------|---------------|------------|
| [claim] | [source] | Observed/Inferred/Hypothesized | High/Medium/Low |

## Open Evidence Gaps
- [gap and what would change the recommendation]
```

## Constraints

- Use PMF Engine only for product-exists contexts with real user/customer evidence. Do not fabricate PMF signal from market research or founder hypotheses.
- Do not treat the 40% very-disappointed threshold as a standalone verdict; cross-check it against sample quality, retention, engagement, and segment viability.
- Preserve the distinction between customer, buyer, user, and HXC.
- Ground every segment recommendation, exclusion, and product-focus recommendation in evidence.
- Do not prescribe UI or architecture - describe PMF, segment focus, and customer evidence implications.
- Present findings before writing.
- Do not overwrite existing output without asking the user first.
- This is a child framework skill in the `customer-discovery` Research Session Loop. Do not emit cross-skill or downstream routing from framework stops, and do not recommend execution-loop commands or path-shaped child framework invocations. Inline framework handoff sections must name only the parent command `$customer-discovery`.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/pmf-engine-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
