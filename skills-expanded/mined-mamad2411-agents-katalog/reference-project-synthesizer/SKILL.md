---
name: reference-project-synthesizer
description: Connect structured reference source cards to the active ML project. Use when papers, collaborator docs, Markdown notes, specs, scripts, BibTeX files, or source bundles should inform claims, risks, baselines, benchmarks, experiments, algorithm design, implementation, writing contracts, citations, collaborator actions, project initialization, or memory writeback.
argument-hint: "[project-root] [source-card-or-source-id] [--link-claims] [--benchmark] [--baseline] [--writing] [--risk] [--feedback] [--spec] [--implementation] [--seed-project]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Reference Project Synthesizer

Convert source cards into project decisions. This skill answers: **What does this source mean for our project?**

Use after `reference-reading-summarizer` has produced a source card. Do not repeatedly re-read raw sources unless the card is insufficient or low confidence.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   └── project-link-routing.md
└── templates/
    └── project-use-note.md
```

## Core Contract

- Read project memory before linking a source to claims, experiments, risks, implementation, collaborator actions, or writing.
- Use source cards as compressed inputs. Raw source files and raw reading trajectories stay out of project memory.
- Stronger reasoning is required when the source changes a claim, baseline, benchmark, novelty boundary, implementation plan, collaborator commitment, or project seed.
- Every project implication should link to a source card, confidence level, and target memory object.
- Do not promote a cheap skim into a project decision without marking uncertainty or requesting deeper reading.

## Inputs

Prefer:

- `reference/cards/<source-id>.md`
- `reference/.agent/source-index.md`
- `reference/.agent/processing-status.md`
- backward-compatible `reference/.agent/reference-index.md` and `reading-status.md`
- `memory/current-status.md`
- `memory/claim-board.md`
- `memory/evidence-board.md`
- `memory/risk-board.md`
- `memory/action-board.md`
- `paper/.agent/writing-contract.md`
- `code/.agent/benchmark-plan.md` or equivalent, when present

## Model Routing

Read `references/project-link-routing.md`.

- Tier 2 normal main model: routine project-use notes, citation placement, writing-pattern routing, structured feedback actions.
- Tier 3 strong/deep model: closest-work risk, must-have baseline, benchmark protocol, core algorithm/theory impact, project seed, conflicted collaborator feedback, final positioning.
- Do not use cheap sidecar output as the final authority for project decisions.

## Workflow

1. Locate the project root and existing memory.
2. Read the relevant source card and its confidence/provenance.
3. Identify requested synthesis mode:
   - claim support or challenge
   - baseline implication
   - benchmark/task/protocol implication
   - method/theory implication
   - implementation implication
   - writing pattern
   - citation placement
   - collaborator feedback/action
   - project spec/constraint
   - project seed
   - reviewer-risk or novelty boundary
4. Create or update `reference/project-use/<source-id>.md` from `templates/project-use-note.md`.
5. Write only durable conclusions into project memory — link-mode determines target:
   - claim support/challenge → `memory/claim-board.md` + `memory/evidence-board.md`
   - identified risk or blocker → `memory/risk-board.md` + `memory/action-board.md`
   - baseline or benchmark → code-side `docs/experiments/` or `memory/evidence-board.md`
   - implementation hint → code-side design doc or `memory/decision-log.md`
   - writing exemplar or style pattern → `paper/.agent/writing-memory/` via `paper-writing-memory-manager`
   - reviewer-risk or novelty framing → `memory/risk-board.md` or `paper/.agent/paper-evidence-board.md`
   - provenance link → `memory/provenance-board.md`
6. If the card is too weak, route back to `reference-reading-summarizer` with the required reading mode.

## Output Rules

Each project-use note should include:

- one-line project relevance
- supported or challenged claims
- baseline, benchmark, implementation, or spec implications
- algorithm/theory implications
- writing/citation implications
- collaborator actions if relevant
- risks and actions
- confidence and required follow-up

End with the closure audit:

```text
Goal: What project question did this source help answer?
Answer: What did we learn?
Path: Which card, sections/files, and memory objects support this?
Correctness: Why should we trust it, and what needs deeper reading?
Next: What changes in the project?
```
