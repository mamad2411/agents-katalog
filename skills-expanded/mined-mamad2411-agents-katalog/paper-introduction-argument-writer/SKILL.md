---
name: paper-introduction-argument-writer
description: Plan and draft ML/AI introductions as venue-aware argument chains. Use for hook, gap, insight, method, result, contribution flow, and paragraph roles.
argument-hint: "[paper-dir] [--venue <venue>] [--archetype <type>] [--mode plan|draft|revise]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Paper Introduction Argument Writer

Write introductions as disciplined arguments. This skill turns a paper's positioning, venue, claims, and evidence into a paragraph-by-paragraph introduction plan or draft.

Use this skill for:

- choosing an introduction argument structure for a target venue and paper archetype
- assigning jobs to intro paragraphs
- drafting or revising hook, problem, gap, insight, method, result, and contribution paragraphs
- strengthening contribution bullets without overclaiming
- deciding what related-work contrast belongs in the introduction
- making intro wording consistent with the abstract, title, evidence board, and writing contract

Do not use this skill for full-paper review. Use `paper-reviewer-simulator` for adversarial critique. Use `paper-writing-assistant` for broad prose drafting. Use `paper-writing-memory-manager` to record introduction paragraph roles, claim dependencies, and stale downstream locations. Use `related-work-positioning-writer` for the full related-work section. Use `paper-writing-contract-planner` first when the paper archetype or claim contract is not settled.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── argument-patterns.md
│   └── paragraph-moves.md
└── templates/
    └── introduction-plan.md
```

## Progressive Loading

- Always read `references/argument-patterns.md`.
- Read `references/paragraph-moves.md` when drafting, revising, or diagnosing paragraph-level flow.
- Use `templates/introduction-plan.md` when creating `paper/.agent/introduction-plan.md`.
- Read local `paper/.agent/writing-contract.md`, `paper/.agent/writing-memory/`, `paper/.agent/paper-evidence-board.md`, `paper/.agent/related-work-plan.md`, and `paper/.agent/provisional-results.md` when present.
- Read current draft files such as `main.tex`, `paper.tex`, `sections/introduction.tex`, `sections/intro.tex`, `sections/abstract.tex`, and `sections/related_work.tex` when revising an existing paper.

## Core Principles

- The introduction is a sales argument, not a literature survey.
- Each paragraph needs one reader-facing job and one handoff sentence.
- The gap must be specific enough to justify this paper, not the whole field.
- The insight must explain why the proposed approach is plausible before details appear.
- Result claims in the introduction must match evidence status.
- Contribution bullets should name deliverables and evidence, not repeat marketing slogans.
- Related-work contrast in the introduction should include only the closest boundary needed to understand novelty.
- If the evidence is missing or provisional, narrow the claim or mark the placeholder explicitly.

## Step 1 - Build an Intro Snapshot

Extract:

```markdown
## Introduction Snapshot
- Target venue:
- Paper archetype:
- Intended audience:
- Primary claim:
- Secondary claims:
- Core problem:
- Closest prior limitation:
- Key insight:
- Proposed object:
- Main evidence:
- Missing/provisional evidence:
- Related-work boundary needed in intro:
- Forbidden claims:
```

Prefer existing project artifacts over memory. If no claim IDs exist, assign local `CLM-TMP-*` IDs and suggest syncing them to `paper-evidence-board`.

## Step 2 - Select Argument Pattern

Read `references/argument-patterns.md` and choose one pattern:

- method breakthrough
- benchmark/dataset
- empirical study
- analysis/diagnostic
- systems/tooling
- application
- negative result or limitation
- hybrid

If the paper has multiple plausible archetypes, choose the one that matches the paper's main sell and mark the secondary archetype as a constraint.

## Step 3 - Plan Paragraph Jobs

Create or update:

```text
paper/.agent/introduction-plan.md
```

If there is no `paper/` directory and the current directory is the paper repo, save to:

```text
.agent/introduction-plan.md
```

Use `templates/introduction-plan.md`. Every paragraph should specify:

- paragraph job
- first-sentence role
- evidence or citation used
- claim supported
- handoff to next paragraph
- overclaim risk

## Step 4 - Draft or Revise the Introduction

When drafting, write paragraph-by-paragraph prose that follows the plan. When revising, preserve correct citations, labels, macros, math, and verified numbers.

For each paragraph:

- open with the reader question for that paragraph
- move from known context to paper-specific gap
- use one main contrast, not several unrelated contrasts
- end by pushing the reader to the next paragraph
- avoid final-sounding claims when evidence is provisional

## Step 5 - Contribution Paragraph

Contribution bullets should answer:

- What did we build, prove, evaluate, release, or discover?
- What is the claim strength?
- Which evidence supports it?
- What should the reader remember?

Avoid contribution bullets that only restate section titles.

## Step 6 - Final Checks

Before finalizing:

- intro claim strength matches the evidence board and writing contract
- the gap is neither too broad nor too narrow
- the insight appears before method detail
- related-work contrast is enough but not a full survey
- contribution bullets are concrete and evidence-backed
- all provisional result language is searchable and tracked
- abstract/title alignment issues are routed to `abstract-title-contribution-writer` when needed
- introduction claim, paragraph-role, or handoff changes are written back through `paper-writing-memory-manager`
