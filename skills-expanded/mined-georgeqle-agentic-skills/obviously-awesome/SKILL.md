---
name: obviously-awesome
description: April Dunford Obviously Awesome methodology — 5-step positioning from real customer evidence
type: research
version: v0.9
invocation: sub-skill
parent: positioning
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell, instead of the target skill. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Obviously Awesome — April Dunford Positioning Methodology

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

Applies the full 5-step Obviously Awesome methodology (April Dunford) as a standalone deep-dive framework. While the parent `$positioning` skill uses Obviously Awesome as its primary methodology, this child skill goes deeper with rigorous customer-evidence grounding, multiple candidate evaluations per step, and explicit evidence quality assessment. Requires real customer evidence. Produces an intermediate artifact for the parent `$positioning` synthesis.

## Prerequisites

- **HARD**: `research/customer-feedback.md` (or `research/{slug}/customer-feedback.md`) must exist with real customer evidence (interviews, survey data, support tickets, reviews, or usage data). If not, stop and tell the user: "Obviously Awesome requires real customer evidence. Run `$customer-feedback` first to gather and synthesize customer data, then re-run `$obviously-awesome`."
- **Hard**: `research/icp.md` (or `research/{slug}/icp.md`) must exist. If not, tell the user to run `$customer-discovery` first and stop.
- **Hard**: `research/competitive-analysis.md` (or `research/{slug}/competitive-analysis.md`) must exist. If not, tell the user to run `$competitive-analysis` first and stop.
- **Soft**: Read if they exist:
  - `research/journey-map.md` — value delivery moments
  - `research/positioning-jtbd.md` — job framing for context
  - `research/positioning-strategic-canvas.md` — differentiation evidence
  - `research/positioning-moore.md` — hypothesis to validate against
  - `research/positioning.md` — existing positioning to improve upon

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

- Read `research/customer-feedback.md` — this is the PRIMARY input. Extract:
  - What customers say they switched from (competitive alternatives)
  - What customers say is different about this product (unique attributes)
  - What value customers report getting (in their own words)
  - Who the happiest/most engaged customers are (target segment signals)
  - How customers describe the product to others (market category clues)
- Read `research/icp.md` — segments, pain points
- Read `research/competitive-analysis.md` — landscape context
- Read prior framework outputs if available

### 2. Step 1 — Competitive Alternatives (Customer-Evidenced)

Unlike the parent skill's broad approach, ground competitive alternatives exclusively in customer evidence:

- What did current customers use BEFORE this product?
- What would they switch to if this product disappeared?
- What do prospects compare this product to during evaluation?

Sources (from customer-feedback.md):
- Switch stories: "I used to use [X] but..."
- Comparison mentions: "Compared to [X], this..."
- Evaluation context: "I was looking at [X] and [Y] when..."

Present findings. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "These are the competitive alternatives customers actually mention. Any that are missing from our customer data that you know prospects consider?"

### 3. Step 2 — Unique Attributes (Customer-Validated)

For each competitive alternative, identify attributes customers explicitly value that alternatives lack:

- Only include attributes customers have MENTIONED or demonstrated through behavior
- Exclude attributes the team believes are unique but customers haven't validated
- Distinguish between "mentioned unprompted" (strong) and "agreed when asked" (moderate)

| Attribute | Customer Evidence | Strength | Alternative Lacking |
|-----------|------------------|----------|-------------------|
| [attribute] | [exact quote or behavior] | Unprompted/Prompted | [which alternatives] |

If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "These are attributes customers validate as unique. Any proprietary capabilities that customers haven't articulated but demonstrably use?"

### 4. Step 3 — Value Mapping (Customer Words)

Map each unique attribute to the value customers report, using their language:

| Unique Attribute | Customer-Stated Value | Customer Quote | Value Type |
|-----------------|----------------------|----------------|------------|
| [attribute] | [value in their words] | "[exact quote]" | Time/Money/Risk/Capability/Quality |

Identify the **primary value cluster** — the value theme that appears most frequently across customer segments.

### 5. Step 4 — Target Segment (Best-Fit Customers)

From customer evidence, identify who gets the most value:

- Which customers are most engaged/retained?
- Which customers would be most disappointed without the product?
- Which customers refer others most frequently?
- What do these best-fit customers have in common?

Define the segment with observable, actionable characteristics (not demographics alone):
- Company stage, size, or type
- Specific pain or trigger event
- Technology stack or workflow context
- Buying behavior or evaluation pattern

If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "This is the segment the customer data supports as best-fit. Does it match your retention and expansion data?"

### 6. Step 5 — Market Category (Customer Framing)

How do customers describe what this product IS?

- How do they explain it to colleagues?
- What category do they put it in mentally?
- What search terms did they use to find it?
- What budget does it come from?

Evaluate market category options:
| Category Option | Customer Evidence | Competitive Context | Trade-off |
|----------------|------------------|--------------------|-----------|
| [option] | [how customers frame it] | [who you'd compete against] | [what you gain/lose] |

Use WebSearch (2-3 queries) to validate category framing externally.

### 7. Synthesize and Assess Evidence Quality

Combine all five steps and explicitly rate evidence quality:

| Step | Conclusion | Evidence Quality | Confidence | Gap |
|------|-----------|-----------------|------------|-----|
| Competitive alternatives | [summary] | [Strong/Moderate/Weak] | [H/M/L] | [what's missing] |
| Unique attributes | [summary] | [S/M/W] | [H/M/L] | [gap] |
| Value | [summary] | [S/M/W] | [H/M/L] | [gap] |
| Target segment | [summary] | [S/M/W] | [H/M/L] | [gap] |
| Market category | [summary] | [S/M/W] | [H/M/L] | [gap] |

Present full synthesis. If the session is already in Plan mode, prefer `request_user_input`; otherwise ask in plain text:
- "Here is the complete Obviously Awesome analysis grounded in customer evidence. Which steps have weak evidence that needs strengthening before this feeds into final positioning?"

### 8. Write Output

Only after user approval.

## Output

### `research/positioning-obviously-awesome.md` (or `research/{slug}/positioning-obviously-awesome.md`)

```markdown
# Obviously Awesome Positioning Analysis

> Based on: research/customer-feedback.md, research/icp.md, research/competitive-analysis.md
> Date: [current date]
> Methodology: Obviously Awesome (April Dunford) — customer-evidence-grounded
> HARD PREREQ: real customer evidence in customer-feedback.md

## Evidence Quality Summary

| Step | Evidence Quality | Sample Size | Confidence |
|------|-----------------|-------------|------------|
| Competitive alternatives | [S/M/W] | [n customers] | [H/M/L] |
| Unique attributes | [S/M/W] | [n mentions] | [H/M/L] |
| Value | [S/M/W] | [n data points] | [H/M/L] |
| Target segment | [S/M/W] | [n customers in segment] | [H/M/L] |
| Market category | [S/M/W] | [n category signals] | [H/M/L] |

## Step 1: Competitive Alternatives (Customer-Evidenced)

| Alternative | How Customers Mention It | Frequency | Context |
|-------------|-------------------------|-----------|---------|
| [alt] | "[customer quote]" | [n mentions] | [switch/compare/evaluate] |

**Primary alternative**: [most frequently mentioned]

## Step 2: Unique Attributes (Customer-Validated)

| Attribute | Customer Evidence | Signal Strength | Alternatives Lacking |
|-----------|------------------|-----------------|---------------------|
| [attribute] | "[quote]" | Unprompted/Prompted | [which] |

**Excluded (unvalidated by customers)**:
- [attribute team believes is unique but customers haven't confirmed]

## Step 3: Value Mapping (Customer Words)

| Unique Attribute | Customer-Stated Value | Quote | Value Type |
|-----------------|----------------------|-------|------------|
| [attr] | [value] | "[exact words]" | [type] |

**Primary value cluster**: [theme]

## Step 4: Best-Fit Target Segment

**Segment definition**: [observable characteristics]
**Evidence**: [engagement, retention, referral data]
**Common traits**:
- [trait 1]
- [trait 2]
- [trait 3]

**Alignment with ICP**: [how this narrows or confirms the ICP]

## Step 5: Market Category

**Recommended category**: [name]
**Customer framing evidence**: [how they describe it]
**Strategy**: [existing/subcategory/new]

### Categories Considered

| Category | Customer Evidence | Competitive Implication | Verdict |
|----------|------------------|------------------------|---------|
| [category] | [evidence] | [who you'd face] | [chosen/rejected + why] |

## Positioning Hypothesis (Obviously Awesome Format)

**For** [target segment from step 4]
**who** [primary need evidenced in customer feedback]
**[product] is a** [market category from step 5]
**that** [primary value cluster from step 3]
**Unlike** [primary alternative from step 1]
**[product]** [key differentiation from step 2]

## Evidence Gaps and Recommendations

| Gap | Impact | How to Fill |
|-----|--------|-------------|
| [what's missing] | [how it weakens positioning] | [specific action] |

## Implications for Positioning Synthesis

[How this customer-grounded analysis should influence the final positioning — where it confirms or challenges other framework outputs, and what it means for the canonical positioning statement]
```

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable work goes in `tasks/todo.md`.
- Human-only external actions go in `tasks/manual-todo.md` with blocking/dependency annotations.
- Condition-gated records go in `tasks/record-todo.md`.
- Cadence-based reviews go in `tasks/recurring-todo.md`.

## Constraints

- **HARD PREREQUISITE: real customer evidence.** CANNOT run without `research/customer-feedback.md` containing actual customer data. Do not proceed with hypothetical or team-assumed customer perspectives.
- **Intermediate artifact only.** This produces `research/positioning-obviously-awesome.md`, not the canonical `research/positioning.md`.
- **Customer words over team assumptions.** Every finding must trace to customer evidence. Flag anything that relies on team belief alone.
- **Evidence quality is explicit.** Rate and display confidence for every step. Weak evidence is a finding, not a failure.
- **Present before writing.** Never write output files until findings are validated.
- **Distinguish signal strength.** Unprompted customer mentions are stronger than prompted agreement.
- **Do not conflate with parent skill.** The parent `$positioning` uses Obviously Awesome lightly; this child skill does it rigorously with full customer grounding.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/obviously-awesome-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
