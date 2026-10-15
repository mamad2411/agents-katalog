---
name: paper-positioning-planner
description: Decide what an ML or AI paper should strategically sell before detailed writing or venue-specific polishing. Use this skill whenever the user has an idea, literature map, experiment results, figures, reviewer risks, or a draft and needs to choose the paper's primary contribution, claim scope, paper archetype, target audience, novelty framing, related-work boundary, title/abstract/main-figure story, or claims to avoid before using conference-writing-adapter.
argument-hint: "[project-dir-or-paper-draft] [--venue <venue>] [--mode early|midproject|draft|revision|rebuttal]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Paper Positioning Planner

Decide what the paper is selling, to whom, against which closest work, and with what evidence.

Use this skill when:

- a project has enough idea/literature/evidence to ask what the paper should be
- results are mixed and the contribution type may need to change
- a draft feels unfocused or overclaims beyond evidence
- figure review or reviewer simulation suggests the paper story is wrong
- the user needs a primary claim, secondary claims, title/abstract direction, intro thesis, or related-work boundary
- the paper may be a method paper, theory-guided method, empirical analysis, benchmark, diagnostic paper, systems paper, or negative/limitation paper
- the user is deciding between target audiences or venues before polishing the text

Do not use this skill as a paragraph-level writing adapter. Use `conference-writing-adapter` after the positioning decision is clear.

Pair this skill with:

- `research-idea-validator` when the whole project may need pursue/revise/park/kill
- `literature-review-sprint` when closest work or community framing is unclear
- `algorithm-design-planner` when the chosen position changes the method specification
- `baseline-selection-audit` when the position depends on whether comparisons are reviewer-proof
- `figure-results-review` when visual evidence changes claim scope
- `paper-evidence-board` when positioning decisions must update claim/evidence/risk/action links
- `paper-reviewer-simulator` after positioning to stress-test the selected story
- `conference-writing-adapter` after positioning to rewrite sections for the target venue
- `research-project-memory` when positioning decisions should persist across sessions

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── audience-venue-fit.md
    ├── contribution-claim-map.md
    ├── decision-rules.md
    ├── memory-writeback.md
    ├── narrative-architecture.md
    ├── positioning-taxonomy.md
    └── report-template.md
```

## Progressive Loading

- Always read `references/positioning-taxonomy.md`, `references/contribution-claim-map.md`, and `references/decision-rules.md`.
- Read `references/audience-venue-fit.md` when target venue, audience, or community framing matters.
- Read `references/narrative-architecture.md` when producing title, abstract, intro, related-work, or main-figure direction.
- Read `references/report-template.md` before writing the final positioning report.
- Read `references/memory-writeback.md` when the project has `memory/`, component `.agent/` folders, or the user asks for persistent memory.
- If the position depends on current venue expectations or recent accepted papers, verify with current sources, OpenReview, proceedings, or user-provided exemplars.

## Core Principles

- Positioning is a decision, not a list of possible stories.
- The primary contribution must be supported by the strongest evidence, not by the user's favorite idea.
- A smaller true claim is stronger than a broad brittle claim.
- Secondary contributions should reinforce the primary story, not compete with it.
- Closest work defines the novelty boundary and the reviewer attack surface.
- The title, abstract, intro thesis, main figure, and result table should all sell the same core story.
- Claims to avoid are as important as claims to emphasize.
- A positioning decision should route concrete changes to writing, experiments, figures, or method design.

## Step 1 - Recover Project State

Collect:

- one-sentence project idea or current paper thesis
- target venue or audience, if known
- current paper draft, outline, abstract, title, figures, or result tables
- literature map and closest-work risks
- baseline audit or missing-comparison risks
- figure/results review outcomes
- reviewer simulation or real review concerns
- available evidence and unsupported claims
- project memory IDs such as `CLM-###`, `EVD-###`, `RSK-###`, `ACT-###`, `FIG-###`, or `TAB-###`

Write the current story as:

```text
This paper sells [primary contribution] to [audience] by showing [evidence] against [closest work], while avoiding the claim that [unsupported overclaim].
```

If the sentence cannot be written, the likely decision is `revise-positioning`.

## Step 2 - Choose Paper Archetype

Read `references/positioning-taxonomy.md`.

Choose one primary archetype:

- method paper
- theory-guided method
- empirical analysis
- benchmark or dataset
- systems or tooling
- application paper
- diagnostic or mechanistic study
- negative result or limitation paper
- position or perspective paper
- hybrid paper

State why other plausible archetypes are weaker. Do not let the paper be a vague hybrid unless the evidence truly supports two linked contributions.

## Step 3 - Map Contributions to Evidence

Read `references/contribution-claim-map.md`.

Create:

- primary contribution
- secondary contributions
- claims to keep
- claims to narrow
- claims to cut
- evidence required for each claim
- evidence currently available
- closest-work distinction
- reviewer risk if the claim stays

Every primary claim must have at least one strong evidence route. If no route exists, revise the paper archetype or route to more experiments.

## Step 4 - Decide Audience and Venue Fit

Read `references/audience-venue-fit.md` when relevant.

Decide:

- who should care first: method researchers, theorists, benchmark users, systems builders, application researchers, or empirical analysts
- which community's standards define novelty and evidence
- whether the target venue is compatible with the strongest story
- what the paper should not try to satisfy
- what related-work boundary is needed to prevent reviewer confusion

If the evidence fits a different audience better than the user's target venue, say so directly and give the least disruptive repositioning.

## Step 5 - Select the Strategic Position

Read `references/decision-rules.md`.

Choose exactly one:

- `lock-position`: story is coherent; proceed to writing adaptation
- `revise-positioning`: core contribution remains, but title/abstract/claims/figures must shift
- `narrow-claim`: evidence supports a smaller paper than the current draft claims
- `change-archetype`: paper type should change, such as method to empirical analysis or diagnostic study
- `need-evidence`: positioning depends on missing experiment, baseline, figure, theorem, or literature check
- `park-paper`: current evidence does not support a viable paper story yet

Do not choose `lock-position` if closest-work, baseline, or figure evidence risks remain fatal.

## Step 6 - Build Narrative Architecture

Read `references/narrative-architecture.md`.

Produce:

- candidate title direction
- one-sentence thesis
- abstract skeleton
- intro paragraph roles
- main figure or main table role
- result-section ordering
- related-work boundary
- limitations to state proactively
- claims to avoid

This should be strategic and section-level. Use `conference-writing-adapter` later for paragraph-level venue writing.

## Step 7 - Route Changes

Route every unresolved issue:

- `conference-writing-adapter`: position is clear and text needs venue-specific rewriting
- `paper-evidence-board`: claims/evidence/figures/risks must be synchronized
- `figure-results-review`: main figure/table does not support the selected story
- `baseline-selection-audit`: selected story needs stronger comparison defense
- `experiment-design-planner`: missing evidence must be planned
- `result-diagnosis`: negative or mixed results threaten the position
- `literature-review-sprint`: closest-work boundary remains unclear
- `algorithm-design-planner`: method needs to change to fit the selected claim

## Step 8 - Write the Positioning Report

Read `references/report-template.md`.

If saving to a project and no path is given, use:

```text
docs/paper/positioning_plan_YYYY-MM-DD_<short-name>.md
```

The report must include:

- current story diagnosis
- selected paper archetype
- positioning decision
- primary and secondary contributions
- claim/evidence map
- closest-work and audience boundary
- narrative architecture
- claims to avoid
- routed actions and next skills
- memory update section

## Step 9 - Write Back to Project Memory

Read `references/memory-writeback.md` when memory exists.

Update the smallest useful set of entries:

- `memory/decision-log.md`: selected paper position, archetype, target audience, and revisit triggers
- `memory/claim-board.md`: claims kept, narrowed, revised, cut, or blocked
- `memory/evidence-board.md`: evidence required by the selected story
- `memory/risk-board.md`: positioning, closest-work, overclaim, audience, and evidence risks
- `memory/action-board.md`: writing, figure, experiment, baseline, or literature actions
- `paper/.agent/`: title/abstract/main-figure/section positioning notes

Use certainty labels:

- `verified` for evidence checked against results, draft text, or sources
- `user-stated` for user goals and constraints
- `inferred` for strategic judgments and reviewer-risk predictions
- `unverified` for positions depending on unchecked current literature or missing results

## Final Sanity Check

Before finalizing:

- one primary story is selected
- paper archetype is explicit
- audience and closest-work boundary are clear
- every primary claim has evidence or a routed action
- unsupported claims are named and removed/narrowed
- title/abstract/main-figure direction match the same story
- next skill is unambiguous
- project memory is updated when present
