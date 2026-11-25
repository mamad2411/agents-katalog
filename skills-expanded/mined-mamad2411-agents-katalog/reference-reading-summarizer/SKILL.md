---
name: reference-reading-summarizer
description: Read and summarize project reference sources into structured source cards. Use for skimming papers, PDFs, Word docs, Markdown notes, BibTeX files, scripts, specs, collaborator feedback, or source bundles; extract writing patterns, methods, theory, benchmarks, baselines, implementation hints, risks, constraints, and project seeds without yet deciding project implications.
argument-hint: "[project-root] [source-id-or-path] [--mode skim|extract-writing|extract-method|extract-theory|extract-benchmark|extract-baseline|extract-risk|extract-feedback|extract-spec|extract-bundle|extract-implementation-hints|extract-project-seed|deep-read]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Reference Reading Summarizer

Turn a reference source into a structured, copyright-safe source card. This skill answers: **What does this source say?**

Do not force every source into project decisions. Use `reference-project-synthesizer` after a card exists and the project implication matters.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── model-routing.md
│   └── reading-modes.md
└── templates/
    ├── source-card.md
    ├── paper-card.md
    └── reading-run.md
```

## Core Contract

- Read to the requested purpose, not exhaustively by default.
- Use cheaper models for skim and routine extraction; escalate for central method, theory, benchmark, closest-work, final-paper claims, or collaborator decisions.
- Preserve provenance: source path, source type, pages/sections/files inspected, reading mode, model tier, confidence, and reviewer status.
- Do not paste long raw source text into cards. Summarize and point to pages/sections/files.
- Separate source content from project implications.

## Source Types

- `paper-or-pdf`: paper PDFs, reports, slide exports, or other PDF references
- `collaborator-doc`: PDF/Word/text feedback or collaborator-authored notes
- `markdown` / `text-note` / `latex-source`: notes, specs, drafts, or design documents
- `bibliography`: BibTeX collections and citation sets
- `script` / `notebook` / `config-or-spec`: implementation hints, protocols, task definitions
- `bundle`: folder containing multiple docs/scripts/bib/configs that should be interpreted as a unit

## Reading Modes

- `skim`: relevance, role labels, whether deeper reading is needed
- `extract-writing`: intro framing, paragraph moves, contribution wording, captions, figure/table narration
- `extract-method`: algorithm, objective, architecture, inference, implementation details
- `extract-theory`: assumptions, theorem statements, proof ideas, formal definitions
- `extract-benchmark`: task, dataset, split, metric, protocol, compute, evaluation caveats
- `extract-baseline`: baseline method role, fairness conditions, comparison requirements
- `extract-risk`: closest-work threat, novelty boundary, reviewer attack surface
- `extract-feedback`: collaborator comments, requested edits, contradictions, decisions, TODOs
- `extract-spec`: requirements, constraints, interfaces, acceptance criteria, project assumptions
- `extract-bundle`: bundle inventory, internal relationships, most useful files, missing context
- `extract-implementation-hints`: reusable scripts, configs, APIs, preprocessing, commands, pitfalls
- `extract-project-seed`: initial idea, problem, assumptions, resources, open questions, first actions
- `deep-read`: high-value source where misunderstanding would change project direction

## Model Routing

Read `references/model-routing.md`.

Default:

- Tier 0 deterministic tools: metadata, file inventory, page/text extraction, bundle manifest
- Tier 1 cheap sidecar: `skim`, simple card skeleton, writing-pattern extraction, bundle inventory
- Tier 2 normal main model: benchmark/protocol extraction, method extraction, collaborator feedback structuring, citation support
- Tier 3 strong/deep model: core theory, closest work, must-have baseline, final paper claims, project seed, collaborator decision conflict

Escalate when the source is closest work, a core algorithm source, a theory source, a benchmark source, a project seed, a collaborator constraint, or when the card will support a claim, experiment, baseline, implementation, paper revision, or rebuttal.

## Workflow

1. Locate `reference/.agent/source-index.md` first; fall back to `reference/.agent/reference-index.md`.
2. Identify the source path, source type, and requested reading mode.
3. Create a run artifact under `reference/.agent/runs/<run-id>/` when extraction is nontrivial:
   - `input-manifest.md`
   - `extraction-notes.md`
   - `model.json`
   - `decision.md`
4. Extract only the needed text/pages/files. Prefer local tools; if unavailable, proceed from available metadata and mark limitations.
5. Fill `templates/source-card.md` into `reference/cards/<source-id>.md`. For pure papers, `templates/paper-card.md` remains a compatible subtype.
6. Update `reference/.agent/processing-status.md` from `unread` or `skimmed` to `carded` when appropriate; update `reading-status.md` if present for compatibility. Memory writeback: this skill writes only to `reference/cards/` and `reference/.agent/`; project-level memory writeback (claim/evidence/risk boards) is the job of `reference-project-synthesizer` after synthesis.
7. Route:
   - project implications needed -> `reference-project-synthesizer`
   - broad field map needed -> `literature-review-sprint`
   - citation coverage needed -> `citation-coverage-audit`

## Source Card Rules

Every card should include:

- metadata and source type
- reading mode
- role labels
- summary or extracted content only as relevant
- limitations and uncertainty
- reusable assets
- provenance and confidence

Do not turn cheap skim cards into strong conclusions. Mark `confidence: skim` or `needs-deep-read` when appropriate.
