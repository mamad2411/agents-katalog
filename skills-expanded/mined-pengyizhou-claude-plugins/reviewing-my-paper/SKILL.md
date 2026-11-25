---
name: reviewing-my-paper
description: Use when the user asks you to review, critique, proofread, or give feedback on their own academic paper or manuscript (usually a PDF), or to mark up review comments directly on the paper.
---

# Reviewing My Paper

## Overview

A multi-lens review pipeline for the user's **own** academic paper that ends in an **annotated PDF** (highlights + sticky notes), not just prose feedback. It layers several independent lenses and — critically — **adversarially verifies its own findings before presenting them**, because a single review pass overstates claims and misses whole categories (citation existence, English discourse flow, figure–text consistency, copy-edit).

**Core principle:** every finding must be *located* (page + anchor) and *verified* before it reaches the PDF. Findings you can't substantiate get dropped or downgraded.

## When to Use

- "Review / critique / give feedback on my paper", "mark up my PDF", "proofread my manuscript".
- The artifact is the user's own paper (be a constructive reviewer, not a gatekeeper).
- NOT for reviewing someone else's paper for a venue (use `academic-research-skills:academic-paper-reviewer` directly) or writing a new paper (`academic-research-skills:academic-paper`).

## Pipeline

Run these in order. Lenses 3–7 are independent → dispatch them as **parallel subagents**, each writing its results to a file so the annotation step can consume them.

| # | Phase | How |
|---|-------|-----|
| 0 | **Extract text** | PyMuPDF (see Environment). Save to `paper_text.txt` with page markers. Large PDFs: don't try to Read all pages. |
| 1 | **Field analysis** | Identify discipline, method type, and *target venue* to calibrate standards. |
| 2 | **Multi-perspective review** | Invoke **`academic-research-skills:academic-paper-reviewer`** (EIC + 3 reviewers + Devil's Advocate + synthesis). |
| 3 | **Citation hallucination check** | Fan out parallel agents over **every** reference (~8 each). Each verifies existence + metadata via WebSearch against DOI / ACL Anthology / OpenReview / proceedings — **never from memory**. Classify VERIFIED / SUSPECT / NOT_FOUND with the 5-type taxonomy (TF/PAC/IH/PH/SH). Mirrors `academic-research-skills:academic-pipeline` integrity_verification_agent. |
| 4 | **Argument / logical flow** | Motivation→method→claim chain, claim-evidence alignment, overclaims, non-sequiturs. |
| 5 | **Academic-English discourse & language precision** | Two levels, both REQUIRED. **Discourse:** general→specific, topic-sentence-first paragraphs, given-before-new cohesion, CARS intro moves, section-opener signposting, cross-section consistency. **Language precision** (the highest-value differentiator — baseline reviewers and the discourse pass *both* skip it): every coined term/jargon defined on first use; one concept = one name across title/abstract/body/index terms; no mechanism restated in vaguer terms or 3+ jargon stacks; flag synonym churn, key-term over-repetition, vague hedges, and forward-references. **Run the [Language & Terminology Audit](#language--terminology-audit-lens-5--required) below — do not stop at discourse-level flow.** |
| 6 | **Figure & table review** | **Render every figure to an image and look** — text extraction (Lens 0) cannot see figures, so they get silently skipped. Three layers: **(a) mismatch** — every number/label/unit/class-name/symbol in a figure matches the text, tables, and body notation; **(b) claim justification** — does the figure actually support the claim it is cited for (a *motivation* figure should embody the method's core idea; a *results* figure should show the effect/trend/significance the text asserts; a *framework* figure should match the pipeline step-for-step)?; **(c) design & improvement cues** — standalone readability, clutter/redundancy, print/grayscale legibility, missing dispersion/CIs/significance. Give concrete improvement cues, not just diagnoses. See [Figure & Table Review](#figure--table-review-lens-6--required). |
| 7 | **Grammar / copy-edit** | Genuine prose errors only. **Tell the agent to ignore PDF-extraction artifacts** (mid-word hyphenation, mangled math/symbols, spaced numerals like "15 696"). |
| 8 | **Adversarial self-verification** | Before finalizing: re-check substantive claims, *especially external facts* (SOTA numbers, prior-art priority, "missing baseline X"), with refute-style subagents. Downgrade or drop anything you can't substantiate. Check disclosed caveats before calling a number an "inconsistency". |
| 9 | **Annotate the PDF** | Build a findings JSON, run `annotate_pdf.py` (see Tool). Color = severity. |
| 10 | **Deliver** | Send the annotated PDF + a short summary. Offer a consolidated P0/P1/P2 revision plan. |

## Environment

PDF tooling is often missing. If `pdftoppm`/`pymupdf` are absent:
```bash
python3 -m venv /tmp/pdfvenv && /tmp/pdfvenv/bin/pip install pymupdf
```
Extract text:
```python
import fitz; doc = fitz.open("paper.pdf")
open("paper_text.txt","w").write("".join(
    f"\n===== PAGE {i+1} =====\n"+p.get_text() for i,p in enumerate(doc)))
```
Render a figure/page to an image (for Lens 6 — figures are invisible to text extraction):
```python
pix = doc[PAGE0].get_pixmap(matrix=fitz.Matrix(3,3))   # PAGE0 is 0-based; 3x ≈ 216 dpi
pix.save("figN.png")                                    # dense figure? crop: clip=fitz.Rect(x0,y0,x1,y1)
```

## Tool: annotate_pdf.py

Findings JSON = list of `{"page": <1-based>, "anchor": "<short unique text>", "severity": "<critical|major|minor|strength|copyedit|clarify>", "note": "<comment>"}`.
```bash
/tmp/pdfvenv/bin/python annotate_pdf.py --src paper.pdf --findings findings.json
```
It highlights the anchor, attaches the note as a popup + comment icon, color-codes by severity, auto-versions the output filename, and prints FOUND/MISSED. Anchor rules: short and unique (a number, heading, or 2–4 words); avoid the first word after a drop-cap; multi-line phrases often miss.

## Annotation conventions

- **Color = severity:** 🔴 critical · 🟠 major · 🔵 minor/clarify · 🟢 strength · 🟣 copy-edit. Always include strengths — balanced feedback.
- Tag each note with its lens, e.g. `[R2 - MAJOR]`, `[EN-Flow - MAJOR]`, `[Copy-edit]`, `[Integrity - STRENGTH]`.
- **Versioned output filename** every iteration (`_v2`, `_v3`…) — same-named files get cached by PDF viewers and the user sees stale comments.

## Language & Terminology Audit (Lens 5 — required)

A word/phrase-level pass *in addition to* discourse flow. **Concentrate it on the Abstract and Introduction**, where these defects cluster and cost the most. The discourse-flow check (topic sentences, cohesion, CARS) does **not** catch these — run this explicitly. Flag and locate (page + anchor) each of:

- **Undefined-on-first-use.** Any coined term or domain jargon used before it is defined — *especially the paper's own invented terms* (e.g., a model the authors call "the reader") that a fresh reader misparses. Require a definition at first occurrence.
- **Term drift / one-concept-many-names.** The same concept named differently across **title, abstract, body, figures, and index terms**. Pick one canonical term; list every variant and where it appears.
- **Over-explanation / restatement.** The same mechanism described 2+ times, each vaguer; jargon stacks of 3+ piled modifiers ("implicit query-to-reference acoustic delta"). Collapse to one plain statement.
- **Redundancy / synonym churn.** Count repetitions of key nouns; flag synonyms used for the *same* object (e.g., "anchor" vs "baseline"). Standardize.
- **Vague hedges / unsupported qualifiers.** "SOTA-level", "setting-dependent", "promising", "flexible and effective" — require they be made precise or scoped.
- **Forward-references.** Abstract/intro contrasting against a method or baseline only introduced later, so the reader cannot yet parse the benefit.
- **Abstract-as-contract.** Every number in the abstract must match a table cell; every named contribution must appear in the body. (Cross-check with Lens 7.)

**Deliver concrete replacement wording, not just diagnoses** — propose the rewritten sentence/abstract, since the user will act on it directly.

## Figure & Table Review (Lens 6 — required)

Figures are **images, not text** — Lens 0 extraction cannot see them, so they are silently skipped unless you render and look. Render each figure (or the page) to PNG and Read it (see Environment for the snippet). Then review at three layers, and locate each finding by anchoring on the figure's caption label (e.g. `Fig. 2`):

- **(a) Mismatch / consistency.** Every number, axis label, unit, tick, and class name in the figure matches the text and tables (e.g. bar-chart values vs. the reported CVs; emotion classes vs. the label set). Symbols/notation in a diagram match the body and equations (e.g. a figure's `x_r` vs. the text's `x^n_i`). Flag every divergence — this is the figure analogue of *abstract-as-contract*.
- **(b) Claim justification — does the figure earn its place?** Name the claim the figure is cited for, then test whether it actually supports it. A *motivation* figure should **embody the paper's core idea** — if the method is "deviation from a baseline," the figure should *show the deviation*, not just two endpoints. A *results/ablation* figure should show the effect size, trend, or significance the text asserts. A *framework* figure should match the described pipeline step-for-step. Flag figures that are merely adjacent to, not evidence for, the claim.
- **(c) Design & improvement cues.** Standalone readability (acronyms and symbols glossed in a self-contained caption); clutter and redundant boxes; legibility at two-column print size and in grayscale; color semantics; missing dispersion / error bars / CIs / significance on quantitative plots. **Give a concrete fix** ("add an arrow showing the query-to-reference delta"), not just a diagnosis.

Also vet **tables** here: do reported baselines share the paper's exact protocol (same split, label space, decoding), or are the numbers copied from a different setting that makes the comparison apples-to-oranges? (Cross-check with Lens 8.)

## Common Mistakes

- **Skipping lenses 5–7.** A general review covers correctness and citations but silently drops discourse-flow, figures, and copy-edit. Run them all.
- **Reviewing only the extracted text and never looking at the figures.** Figures are images; Lens 0 can't see them, so a text-only pass skips them entirely. Render every figure to PNG and run Lens 6 — mismatch, claim-justification, and design cues.
- **Stopping at discourse flow and skipping word-level language precision.** Topic-sentence / cohesion checks pass right over undefined jargon, over-explanation, and term drift — which concentrate in the Abstract. Run the Language & Terminology Audit explicitly (especially on the abstract) and propose replacement wording.
- **Trusting your own findings.** This session's review overstated SOTA gaps and flagged a disclosed caveat as a "critical inconsistency." Always run lens 8 and *refute* external-fact claims before presenting.
- **Citation check that only re-checks the reviewer's claims.** Verify *every* reference for existence, not just the ones a reviewer questioned.
- **Flagging extraction artifacts as grammar errors.** Warn the grammar agent explicitly.
- **Overwriting the same output PDF.** Version it, or the user reports "it didn't update."
- **Editing the manuscript.** Reviewers produce reports/annotations; never rewrite the author's file.

## Cross-references

- **REQUIRED SUB-SKILL:** `academic-research-skills:academic-paper-reviewer` (phase 2).
- **REQUIRED REFERENCE:** `academic-research-skills:academic-pipeline` integrity_verification_agent (phase 3 model).
- Related: `academic-research-skills:academic-paper` (revision mode) to act on the findings.
