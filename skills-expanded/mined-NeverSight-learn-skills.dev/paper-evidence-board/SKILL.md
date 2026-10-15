---
name: paper-evidence-board
description: Maintain a paper-facing evidence board that aligns claims, experiments, figures, tables, sections, reviewer risks, and next actions during ML/AI paper writing. Use this skill whenever writing exposes missing experiments, new results require paper changes, reviewer simulation reveals evidence gaps, claims need support checks, figures/tables need mapping to claims, or the user wants a live paper evidence board before submission.
argument-hint: "[paper-dir-or-project-root] [--venue <venue>] [--mode build|audit|update|review]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Paper Evidence Board

Maintain the paper-facing view of the research project: which claims the paper makes, what evidence supports them, where they appear, what reviewers may attack, and what actions are needed before submission.

Use this skill when:

- writing reveals that a paper claim lacks evidence
- new experiment results require updating paper narrative, figures, or sections
- review simulation creates experiment or writing actions
- a paper draft needs claim-evidence alignment before submission
- figures and tables need to be mapped to paper claims
- figure/table style needs to be tracked as a writing decision, including palette, markers, symbols, typography, and venue-facing visual conventions
- the user wants a live evidence board for a paper
- the project needs to decide whether a gap requires more experiments, rewriting, narrowing a claim, or cutting material

This skill is more specific than `research-project-memory`: it uses project memory as the source of cross-component truth, but creates a paper-facing board for writing and review decisions.

Pair this skill with:

- `research-project-memory` for project-level claim/evidence/risk/action IDs and writeback
- `conference-writing-adapter` when the board shows structural or paragraph-level writing changes
- `experiment-design-planner` when the board exposes missing evidence requiring new experiments
- `result-diagnosis` when new evidence weakens or complicates a claim
- `paper-reviewer-simulator` when the board should be stress-tested from a reviewer perspective
- `figure-results-review` when figures/tables need claim-support, caption, statistical, or visual-style review
- `citation-coverage-audit` when novelty or related-work gaps appear

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── board-schema.md
    ├── evidence-gap-triage.md
    ├── paper-section-map.md
    ├── report-template.md
    ├── reviewer-risk-integration.md
    └── update-protocol.md
```

## Progressive Loading

- Always read `references/board-schema.md`, `references/evidence-gap-triage.md`, and `references/update-protocol.md`.
- Read `references/paper-section-map.md` when building a section-by-section board from a draft.
- Read `references/reviewer-risk-integration.md` when using reviewer simulation, real reviews, or venue-specific risks.
- Use `references/report-template.md` for substantial board reports.
- Verify current venue rules or reviewer forms when venue-specific evidence expectations matter.

## Core Principles

- Every major paper claim should have a paper location, evidence status, and reviewer risk.
- Evidence should point to source artifacts, not only prose memory.
- A figure/table should have a job: support a claim, answer a reviewer question, or delimit scope.
- A paper-facing figure/table should also obey the paper's visual style policy, not just display correct numbers.
- Missing evidence is not a writing problem by default; it may require experiment design, result diagnosis, claim narrowing, or citation work.
- Do not hide negative or weak results. Mark how they change the claim.
- Keep the board actionable: each open gap should route to a next skill or action.

## Step 1 - Locate Paper and Project Memory

Find:

- paper root: `paper/`, current directory, or user-provided path
- project root, if different
- `memory/claim-board.md`
- `memory/evidence-board.md`
- `memory/risk-board.md`
- `memory/action-board.md`
- `paper/.agent/paper-status.md`
- paper sources such as `main.tex`, `paper.tex`, `sections/*.tex`, figures, tables, and appendix

If project memory is missing, still build a paper board from the draft, but recommend initializing `research-project-memory`.

## Step 2 - Extract Paper Claims

Read the draft or provided notes and extract:

- title and abstract claims
- introduction contribution bullets
- method claims
- theory claims
- experiment claims
- related-work novelty boundaries
- limitation and scope claims

Assign or reuse `CLM-###` IDs. For each claim, record:

- exact paper location
- claim type
- strength
- current wording risk
- evidence expected
- evidence available

Do not treat aspirational contribution language as proven evidence.

## Step 3 - Map Evidence to Claims

Read `references/board-schema.md`.

For every evidence item:

- identify source path, run ID, table, figure, theorem, citation, or review text
- link to claim IDs
- mark status: planned, running, observed, reported, stale, contradicted, or cut
- mark certainty: observed, user-stated, inferred, stale, or needs-verification
- state limitations

If evidence is only in a daily log or chat note, mark it accordingly and create an action to verify source artifacts.

## Step 4 - Build Section and Figure/Table Map

Read `references/paper-section-map.md`.

Create:

- section map: section -> claims -> evidence -> risks -> actions
- figure/table map: figure/table -> evidence -> claim -> required caption message -> stale status
- visual style map: palette, method-to-marker mapping, typography, symbols, figure sizing, and table conventions
- appendix map when relevant

Identify:

- claims repeated in multiple places with inconsistent strength
- figures without a claim
- claims without a figure/table/proof/citation when one is expected
- stale figures after new results
- inconsistent colors, symbols, method names, font sizes, or figure sizes across paper visuals
- result tables not discussed in prose

## Step 5 - Triage Evidence Gaps

Read `references/evidence-gap-triage.md`.

For each gap, decide:

- `new-experiment`: needs `experiment-design-planner`
- `result-diagnosis`: existing result is ambiguous or contradictory
- `rewrite`: evidence exists but prose overclaims or hides it
- `narrow-claim`: evidence supports a smaller claim
- `citation-work`: claim needs missing related work or attribution
- `cut`: claim is not worth supporting
- `accept-risk`: limitation can be stated rather than fixed

Every high-risk gap should create an action.

## Step 6 - Integrate Reviewer Risks

Read `references/reviewer-risk-integration.md`.

Use:

- simulated reviewer risks from `paper-reviewer-simulator`
- citation risks from `citation-coverage-audit`
- real review risks from `rebuttal-strategist`
- venue-specific expectations when known

Map each risk to:

- claim
- paper location
- evidence gap
- fix type: experiment, analysis, proof, citation, rewrite, figure/table, limitation, or rebuttal
- priority

## Step 7 - Produce Board and Actions

Use `references/report-template.md` for full output.

If saving to a project and no path is given, use:

```text
paper/.agent/paper-evidence-board.md
```

Output:

- paper snapshot
- claim-evidence matrix
- section map
- figure/table map
- visual style map
- evidence gaps
- reviewer-risk map
- action plan
- project-memory writeback

## Step 8 - Write Back to Project Memory

If the project uses `research-project-memory`, update:

- `memory/claim-board.md`: claim status, wording, paper locations, and weakened/cut claims
- `memory/evidence-board.md`: evidence source paths, figure/table mappings, stale status, and limitations
- `memory/risk-board.md`: evidence-gap, writing, novelty, baseline, and reviewer risks
- `memory/action-board.md`: experiment, diagnosis, rewrite, citation, figure/table, and review actions
- `paper/.agent/paper-status.md`: current paper section state
- `paper/.agent/visual-style.md`: paper-facing figure/table style policy when visual conventions are material
- `paper/.agent/paper-evidence-board.md`: the paper-facing board

Do not duplicate long experiment reports. Link to them.

## Final Sanity Check

Before finalizing:

- every major claim has a location and evidence status
- unsupported claims are marked as planned, narrowed, or cut
- every main figure/table has a claim-facing job
- paper-facing figures/tables share consistent colors, markers, symbols, typography, sizing, and notation
- stale evidence is marked
- reviewer risks link to actions
- next actions are routed to the right skill
- project memory is updated when present
