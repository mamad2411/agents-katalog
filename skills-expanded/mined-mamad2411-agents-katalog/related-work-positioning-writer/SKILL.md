---
name: related-work-positioning-writer
description: Draft ML/AI related work as novelty-boundary writing. Use for closest-work grouping, citation roles, paragraph plans, boundary statements, and safe novelty wording.
argument-hint: "[paper-dir-or-project-root] [--mode plan|draft|revise|audit] [--venue <venue>]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Related Work Positioning Writer

Write related work as a novelty-boundary argument, not as a citation list. This skill turns literature maps, citation coverage audits, positioning decisions, and paper claims into a related-work plan and, when requested, related-work prose.

Use this skill for:

- creating `paper/.agent/related-work-plan.md`
- grouping related work by claim-relevant roles
- deciding which work belongs in the introduction vs related work
- writing topic sentences, synthesis sentences, and boundary sentences
- mapping closest work to novelty risks and safe wording
- avoiding unsupported `first`, `novel`, `unlike prior work`, and `orthogonal` claims
- revising related work after citation coverage or literature review
- aligning related work with the writing contract and paper positioning

Do not use this skill to discover all missing citations from scratch. Use `literature-review-sprint` for field mapping and `citation-coverage-audit` for submission-time missing citation checks. Use `citation-audit` for BibTeX and citation correctness. Use `paper-writing-memory-manager` to record novelty-boundary dependencies and intro/abstract claim impact. Use `paper-writing-assistant` for general paper prose outside related work.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── boundary-patterns.md
│   └── paragraph-recipes.md
└── templates/
    └── related-work-plan.md
```

## Progressive Loading

- Always read `references/boundary-patterns.md`, `references/paragraph-recipes.md`, and `templates/related-work-plan.md`.
- Read `paper/.agent/writing-contract.md` when present.
- Read `paper/.agent/writing-memory/`, `paper/.agent/paper-evidence-board.md`, root `memory/claim-board.md`, and root `memory/risk-board.md` when present.
- Read outputs from `literature-review-sprint`, `citation-coverage-audit`, `paper-positioning-planner`, and `paper-writing-contract-planner` when available.
- Use web search for recent or concurrent work if the user asks for current coverage or if novelty depends on recent papers.

## Core Principles

- Related work should protect the novelty boundary, not inflate it.
- Group by reader question and contribution role, not by chronological list.
- Closest work must be acknowledged directly and fairly.
- Every paragraph needs a synthesis sentence and a boundary sentence.
- Do not cite papers only because they share keywords.
- Do not hide strong prior work in a generic group.
- Safe novelty wording is better than broad "first" claims.
- Related work should reinforce the paper's selected archetype and claims.

## Step 1 - Gather Inputs

Find:

- paper root: `paper/`, current directory, or user-provided path
- current `sections/related.tex`, introduction, contribution bullets, and abstract
- `paper/.agent/writing-contract.md`
- `paper/.agent/related-work-plan.md`
- `paper/.agent/paper-evidence-board.md`
- literature review reports, citation coverage reports, BibTeX files, and citation keys
- closest-work or novelty risks from memory boards

If the literature map is thin and the user asks for a final related-work section, recommend `literature-review-sprint` or `citation-coverage-audit` first.

## Step 2 - Choose Mode

Use:

- `plan`: create or update `related-work-plan.md`
- `draft`: write related-work prose from a plan
- `revise`: edit an existing related-work section for boundary clarity
- `audit`: report novelty-boundary and grouping issues

Default to `plan` when no related-work plan exists and `revise` when a related-work section exists.

## Step 3 - Build Related-Work Buckets

Read `references/boundary-patterns.md`.

Classify cited and candidate work into buckets:

- closest direct work
- same problem, different method
- same method family, different problem
- benchmark/dataset/evaluation work
- theory or analysis foundations
- systems/tooling foundations
- application/domain prior work
- concurrent work
- surveys or taxonomies
- citation-only background

For each bucket, state:

- why this bucket matters
- which paper claim it qualifies
- what boundary sentence is needed
- whether it belongs in introduction, related work, experiments, or appendix

## Step 4 - Define Paragraph Plan

Read `references/paragraph-recipes.md`.

For each related-work paragraph:

```markdown
- Paragraph role:
- Papers included:
- Synthesis sentence:
- Boundary sentence:
- Claim protected:
- Citation keys needed:
- Forbidden wording:
```

Place the closest-work paragraph early unless venue norms strongly favor a different order.

## Step 5 - Write or Update Plan

Use `templates/related-work-plan.md`.

Save to:

```text
paper/.agent/related-work-plan.md
```

If the current directory is the paper repo, save to:

```text
.agent/related-work-plan.md
```

The plan should be useful to `paper-writing-assistant` and `paper-draft-consistency-editor`.
Record changed novelty boundaries and affected intro/title/abstract locations through `paper-writing-memory-manager`.

## Step 6 - Draft or Revise Prose

When drafting:

- write synthesis, not one sentence per citation
- use citation groups only when they share the same role
- state what prior work establishes before saying what remains different
- use safe boundary language
- keep claims aligned with the writing contract

When editing LaTeX:

- preserve citation keys, labels, refs, macros, and comments
- edit the smallest relevant file
- do not add fake citation keys
- if a needed citation key is missing, insert a clear placeholder or report required BibTeX action

## Step 7 - Report Risks and Follow-Ups

Report:

- missing closest-work coverage
- unsafe novelty language
- citation buckets needing more search
- related-work paragraphs that do not protect any claim
- claims that should move to intro, experiments, or limitations

Route:

- `citation-coverage-audit`: missing or recent citations
- `citation-audit`: BibTeX/key correctness
- `paper-writing-contract-planner`: novelty boundary changes the paper contract
- `paper-draft-consistency-editor`: related work conflicts with title/abstract/intro

## Final Sanity Check

- closest work is acknowledged directly
- every paragraph has a synthesis and boundary role
- novelty language is safe and supported
- intro and related work share the same boundary
- no unsupported `first`, `novel`, `unlike prior work`, or `orthogonal` claim remains
- missing citation keys or BibTeX needs are listed
