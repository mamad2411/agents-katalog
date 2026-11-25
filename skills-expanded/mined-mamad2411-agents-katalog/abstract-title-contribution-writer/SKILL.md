---
name: abstract-title-contribution-writer
description: Draft ML/AI paper titles, abstracts, and contribution lists. Use for title options, abstract structure, contribution bullets, and claim-strength calibration.
argument-hint: "[paper-dir] [--venue <venue>] [--archetype <type>] [--mode draft|revise|options]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Abstract Title Contribution Writer

Write the paper's most compressed sales layer: title, abstract, and contribution list. This skill makes the top-level promise clear, concrete, and evidence-calibrated.

Use this skill for:

- generating or revising paper titles
- drafting structured abstracts for target venues and paper archetypes
- writing contribution bullets that match the actual evidence
- checking whether title, abstract, intro, and claims tell the same story
- reducing overclaiming in high-visibility prose
- producing several title/abstract positioning variants for a strategic choice

Do not use this skill for detailed section drafting. Use `paper-introduction-argument-writer` for the introduction, `paper-writing-assistant` for broader prose, `paper-writing-memory-manager` to record top-level claim wording and dependency impact, and `paper-draft-consistency-editor` for full-draft consistency.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── abstract-patterns.md
│   └── title-contribution-rules.md
└── templates/
    └── abstract-title-plan.md
```

## Progressive Loading

- Always read `references/abstract-patterns.md`.
- Read `references/title-contribution-rules.md` when writing titles or contribution bullets.
- Use `templates/abstract-title-plan.md` when creating `paper/.agent/abstract-title-plan.md`.
- Read local `paper/.agent/writing-contract.md`, `paper/.agent/writing-memory/`, `paper/.agent/introduction-plan.md`, `paper/.agent/paper-evidence-board.md`, and `paper/.agent/provisional-results.md` when present.
- Read current `abstract`, `title`, and contribution text from `main.tex`, `paper.tex`, `sections/abstract.tex`, or `sections/introduction.tex` when revising.

## Core Principles

- Title, abstract, and contribution bullets must sell the same paper.
- The abstract is not a shortened introduction; it is a complete claim-evidence contract.
- Title specificity should match evidence strength and audience expectations.
- Contribution bullets should be auditable against figures, tables, theorems, releases, or findings.
- Avoid "first", "novel", "general", "robust", and "state-of-the-art" unless the evidence board supports them.
- If evidence is provisional, write a draft but mark the result placeholder and the required replacement.
- Prefer one clear primary promise over several diluted promises.

## Step 1 - Build Top-Level Snapshot

Extract:

```markdown
## Top-Level Writing Snapshot
- Target venue:
- Paper archetype:
- Primary audience:
- Title currently says:
- Abstract currently says:
- Contribution list currently says:
- Primary claim:
- Main evidence:
- Missing/provisional evidence:
- Forbidden claims:
- Desired positioning variants:
```

If the paper has no stable positioning, route to `paper-positioning-planner` or `paper-writing-contract-planner` before finalizing.

## Step 2 - Select Abstract Pattern

Read `references/abstract-patterns.md` and choose one pattern:

- method
- benchmark/dataset
- empirical study
- analysis/diagnostic
- systems/tooling
- theory
- application
- negative result or limitation

The pattern controls move order, not sentence wording.

## Step 3 - Draft the Abstract Contract

Create or update:

```text
paper/.agent/abstract-title-plan.md
```

If there is no `paper/` directory and the current directory is the paper repo, save to:

```text
.agent/abstract-title-plan.md
```

Use `templates/abstract-title-plan.md`.

For each abstract sentence or clause, record:

- move role
- claim supported
- evidence status
- overclaim risk

## Step 4 - Produce Title Options

Generate three to six title options across useful positioning styles:

- direct method name
- problem-plus-method
- finding-led
- benchmark/resource-led
- mechanism-led
- scoped and conservative

For each title, note what it sells and what risk it creates.

## Step 5 - Write or Revise Contribution Bullets

Each contribution bullet should include:

- concrete deliverable or finding
- scope
- evidence type
- reader value

Contribution bullets should be parallel in grammar and non-overlapping in content.

## Step 6 - Final Checks

Before finalizing:

- title promise appears in abstract and introduction
- abstract claims appear in contribution bullets or paper body
- contribution bullets have evidence locations
- result numbers match verified or explicitly provisional status
- venue-required abstract constraints are respected when known
- title does not oversell generality, novelty, or SOTA
- top-level wording and dependency changes are recorded with `paper-writing-memory-manager`
- open issues are routed to `paper-evidence-board`, `paper-introduction-argument-writer`, or `paper-draft-consistency-editor`
