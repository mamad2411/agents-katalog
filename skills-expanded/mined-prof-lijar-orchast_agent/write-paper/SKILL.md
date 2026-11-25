---
name: write-paper
description: Write a well-structured scientific (SCI/IEEE-style) paper as a PDF about a software system or agent in this repo. Use when the user asks to "write a paper", "write a scientific paper", "SCI paper", "publish a paper PDF", or "document X as a research paper". Grounds every claim in the target's actual source code and renders an IEEE-style two-column PDF with WeasyPrint.
---

# Write a Scientific Paper (PDF)

You are acting as an experienced SCI paper author. Produce a publication-quality,
IEEE-style paper about a target system, grounded **only** in verifiable evidence
(source code, real output artifacts, measurable data). The final deliverable is a
two-column PDF.

## Inputs

- **Subject**: the system/agent the paper is about (e.g. `book-writer/`). Ask if unclear.
- **Authors**: ask the user if not given.
- **Workspace**: `<subject-dir>/paper/` (create `notes/` and `sections/` inside it).

## Non-negotiable rules

1. **Code is the only ground truth.** Never trust generated documentation, README
   marketing, or docs-site pages without confirming against the source. (In this
   repo, `docs_site/agents/*.md` is machine-generated and known to contain
   invented features — see `references/grounding-checklist.md`.)
2. **Every quantitative claim must be measured, not estimated.** Count files, run
   `wc`, inspect artifacts. Record the command used next to the number.
3. **No fabricated citations.** Reference only artifacts you can verify exist:
   project URLs, library documentation, and well-known published work you are
   certain of. Prefer fewer, real references over many plausible ones.
4. **Prose, not bullets**, in the paper body. Bullets are for notes and outlines only.
5. Honest **Limitations** — a paper with no limitations section reads as advertising.

## Workflow (6 phases)

Read `references/paper-structure.md` and `references/style-guide.md` before Phase 2.

### Phase 1 — Study the subject
Read the target's entry points, core modules, configs, and real outputs. Write
`paper/notes/facts.md`: one fact per line, each with a `file:line` citation or the
measurement command. Include: architecture, data flow, prompts/algorithms, external
dependencies, failure handling, and quantitative material (corpus sizes, line
counts, artifact counts, languages, versions). This file is the paper's evidence base.

### Phase 2 — Outline
Write `paper/outline.md` using the IEEE structure in `references/paper-structure.md`.
For each section list: the claims it makes, the evidence (pointers into `facts.md`),
target word count, and planned figures/tables. Total target: 4,500–6,000 words.

### Phase 3 — Draft
Write one Markdown file per section in `paper/sections/` (e.g. `01-introduction.md`).
Academic prose; past tense for what was done, present tense for what the system does.
Figures: inline SVG (architecture/pipeline diagrams) inside a `<figure>` with
`<figcaption>Fig. N. Caption.</figcaption>`. Tables: a caption line
`*TABLE N — Caption*` placed **before** the Markdown table (captions above tables,
below figures), and wrap caption + table together in
`<div class="tablewrap" markdown="1"> … </div>` so column breaks cannot separate
them (`markdown="1"` makes the inner Markdown render; requires the `extra`
extension, which the build script enables). Keep math
minimal and simple — WeasyPrint's MathML rendering handles plain inline
expressions but mangles complex display math (fractions, sums with limits).
Every claim must trace to `facts.md`.

### Phase 4 — Review
Re-read the full draft against this checklist; fix in place:
- [ ] Every claim grounded in `facts.md`; no invented features or numbers
- [ ] Abstract ≤ 250 words, self-contained, states problem/method/results
- [ ] Terminology consistent (one name per concept throughout)
- [ ] Each section delivers what the outline promised
- [ ] Figures/tables are referenced from the text ("Fig. 1 shows…")
- [ ] Limitations are concrete, not token
- [ ] No meta-commentary, TODOs, or outline residue

### Phase 5 — Assemble
Merge into `paper/paper.md`:
```markdown
---
title: "Full Paper Title"
authors: "Author One, Author Two"
affiliation: "Optional affiliation line"
date: "Month Year"
keywords: "kw1, kw2, kw3"
---

## Abstract
...

## Introduction
...
## References
1. Author, "Title," URL or venue, year.
```
Section headings are `##` (they become numbered `I.`, `II.`, … automatically);
subsections `###` (become `A.`, `B.`, …). Do NOT number headings yourself.
Citations in text as `[1]`, matching the numbered References list.

### Phase 6 — Publish
```bash
book-writer/.venv/bin/python <skill-dir>/scripts/build_pdf.py paper/paper.md -o paper/
```
The script auto-versions output (`<slug>-vN.pdf`). Then verify:
1. Exit code 0 and no WeasyPrint layout warnings that matter.
2. Extract text (`pypdf` is available in the venv via its deps, or `pdftotext` if
   installed) and confirm title, authors, all section headings, and references appear.
3. Sane page count (a 5,000-word two-column paper ≈ 6–9 A4 pages).
4. Report the final PDF path to the user.

If a phase's output fails review, loop back — do not push a known-flawed draft
forward. This mirrors the subject repo's own outline → write → review → finalize
pipeline philosophy: separate drafting from quality control.
