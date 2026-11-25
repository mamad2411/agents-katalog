---
name: research-methodology
description: Guides the full academic research workflow for CS/AI/ML/NLP work — finding and organizing related literature, designing a sound study or experiment (datasets, baselines, evaluation metrics, ablations), writing and structuring an academic paper or thesis, and picking the right tools (reference managers, Overleaf, experiment tracking, Git). Use this skill whenever the user is starting or working on a research project, dataset paper, Kaggle/ML experiment meant for publication, thesis, or academic writing — even if they just say "help me with my research" or "how do I write this up" without naming a specific step.
---

# Research Methodology

A practical, end-to-end guide for doing rigorous CS/AI/ML/NLP research — from first literature search to a submittable paper. Built for someone who already codes and runs experiments (e.g. Kaggle/NLP work) but wants a repeatable, structured research process.

## The core loop

Research is rarely linear, but a project usually cycles through these four phases. Each has its own reference file with full detail — read the one that matches where the user is right now.

1. **Literature review** → `references/literature-review.md`
   Find what's already been done, spot the gap your work fills.
2. **Research design** → `references/research-design.md`
   Turn the gap into a testable question, design the dataset/experiment, pick metrics and baselines.
3. **Academic writing** → `references/academic-writing.md`
   Structure and write the paper/thesis, handle citations, target the right venue.
4. **Tools & workflow** → `references/tools-workflow.md`
   Reference managers, Overleaf/LaTeX, experiment tracking, Git — the plumbing that keeps a project reproducible.

## How to use this skill

- If the user names a phase directly ("help me find related work", "how do I write the methodology section"), jump straight to that reference file.
- If they're starting fresh, walk them through the loop in order: help scope a research question first (phase 2 lightly), then go back and do a proper literature review, then flesh out the full design, then write.
- If they already have a draft (paper, dataset, or code) and want feedback, diagnose which phase is weakest before jumping to advice — a weak literature review often looks like a weak methodology section later.
- Always keep advice concrete and actionable: point to a specific search query, a specific metric, a specific section heading — not just abstract principles.

## Quick-start checklist for a new project

Use this as a first pass with the user, then dive into the relevant reference file for depth on any step:

1. Write a one-sentence research question. If it can't be answered "yes/no" or with a number, tighten it.
2. Search 3 sources minimum (e.g. Google Scholar, arXiv, ACL Anthology for NLP) for the last 3–5 years of related work.
3. Build a literature matrix (see `assets/lit-review-tracker-template.csv`) — don't just save PDFs, extract what each paper actually contributes.
4. Identify the gap: what does no existing paper do that this project will?
5. Decide the evaluation: what metric proves the work succeeded, and what's the baseline it must beat?
6. Set up version control and a reference manager before writing a single paragraph (see `references/tools-workflow.md`).
7. Draft the paper outline early (see `assets/paper-outline-template.md`) — writing the shape of the paper before all results are in exposes weak sections sooner.

## Notes for CS/AI/ML/NLP specifically

- A "literature review" for ML work often means checking leaderboards (Papers With Code) and recent arXiv preprints, not just journals — coverage moves faster than formal publication.
- For Bangla/low-resource NLP work specifically, also check ACL Anthology and LREC proceedings, which index most Bangla NLP papers that Google Scholar under-indexes.
- Dataset-driven papers (like MRC or classification datasets) need their own rigor: documented annotation guidelines, inter-annotator agreement, and a clear train/val/test split with no leakage — see `references/research-design.md`.
- If the goal is a Scopus-indexed or Q1 journal, venue choice affects paper structure and length — check `references/academic-writing.md` before writing the first draft, not after.
