---
name: future-scientific-writing
version: 0.1.1
description: >
  Draft and revise scientific manuscripts, abstracts and journal submissions.
  Build an evidence-linked outline, then write clear prose using venue-specific
  structure, citation style, figures and reporting guidelines. Use for IMRAD papers,
  manuscript revision, scientific writing and responses to reviewers.
allowed-tools: Read Write Edit Bash(future:*)
category: methodology
license: MIT license
metadata: {"skill-author": "K-Dense Inc."}
---

# Scientific Writing

Write what the evidence supports, in the format the user and venue require.
Default to connected prose in a manuscript, but allow structured abstracts,
methods lists, hypotheses and other lists required by the journal. Do not extend
manuscript prose rules to slide decks, checklists or a user's requested outline.

## 1. Establish the writing contract

Reuse the user's specified topic, audience, venue, language, length and format.
Identify the manuscript type, source materials, actual study results and missing
inputs. Ask only for unresolved decisions that affect the output. Never invent
experiments, numerical results, ethical approvals, affiliations or consent.

Respect confidential manuscript/reviewer material. Do not upload a private file,
search its private text, submit to a journal or contact authors without appropriate
authorization. Use local materials first when the user provided a closed source set.

## 2. Build an evidence-linked outline

1. Read the supplied results, figures and methods. Distinguish measured findings,
   author interpretations, literature context and information not supplied.
2. For authorized academic lookup, load `future-paper`; for public guidelines or
   source URLs, load `future-web`. Use `future-deep-research` only when substantial
   additional research is requested or necessary within the agreed scope/budget.
   No additional third-party skill is required by this workflow.
3. Verify key citations against original passages. Generated paper summaries and
   snippets help locate sources; they do not establish a manuscript's claims.
   Record title, DOI/PMID or stable URL, passage location and support/limitations.
4. Outline each section with its purpose, main claims, evidence references and
   missing items. Bullet points are useful here; an outline is not a finished paper.
5. Plan the figures/tables around the actual data. Do not generate schematic
   imagery that could be mistaken for an experimental measurement.

## 3. Draft the manuscript

Load `references/imrad_structure.md` when organizing sections. Adapt the structure
for reviews, protocols, case reports, methods papers and the target venue.

- **Methods:** experimental unit, recruitment/selection, randomization, blinding,
  controls, biological versus technical replication, software/data versions,
  exclusions, missingness, ethics and statistical methods. Mark unknowns explicitly.
- **Results:** report the actual observations, denominators, units, effect sizes,
  confidence intervals and relevant tests. Include negative results; separate
  exploratory analyses from prespecified tests. Do not invent missing precision.
- **Discussion:** interpret findings within the design's causal and population
  limits, compare contrary evidence, explain limitations and avoid mechanistic claims
  unsupported by measurements. Distinguish speculation from demonstrated results.
- **Introduction:** establish context, the specific gap and the study objective;
  justify novelty with evidence rather than stock claims of being the first.
- **Abstract/title:** write after the body, reflect its results faithfully, and obey
  the venue's structured/unstructured format and word limit.

Convert the outline into flowing paragraphs with transitions and consistent terms.
Read `references/writing_principles.md` for revision guidance. Treat numerical style
heuristics as suggestions, not universal rules that override the venue or evidence.

## 4. Apply the relevant specialist reference

Read only what the task needs:

| Need | Resource |
|---|---|
| Section purpose and IMRAD alternatives | `references/imrad_structure.md` |
| APA, AMA, Vancouver, Chicago or IEEE citations | `references/citation_styles.md` |
| Figures, captions, tables, units and uncertainty | `references/figures_tables.md` |
| CONSORT, STROBE, PRISMA and other reporting checklists | `references/reporting_guidelines.md` |
| Clarity, terminology and prose revision | `references/writing_principles.md` |
| Optional non-journal LaTeX report styling | `references/professional_report_formatting.md` |

Verify the current guideline/venue requirements when freshness matters. Reference
summaries are topic guides, not official checklist numbering or complete submission
forms; use the actual current checklist (e.g. CONSORT/SPIRIT 2025 and TRIPOD+AI).
A reporting checklist establishes reporting completeness, not methodological validity.

For an explicitly requested professional LaTeX report, the optional assets are
`assets/scientific_report.sty`, `assets/scientific_report_template.tex` and
`assets/REPORT_FORMATTING_GUIDE.md`. Do not force LaTeX or install a TeX distribution
for a Markdown/DOCX request. Follow venue or institutional templates when provided.
Use `future-image` only for authorized illustrative graphics or image analysis.

## 5. Verify the exact delivery

- Check final claims, citations and numerical values against the original inputs;
  drafting can introduce unsupported statements even after a sound outline.
- Reconcile figures/tables with text, denominators, units and uncertainty. Define
  error bars and abbreviations. Follow the requested citation style consistently.
- Check the applicable reporting checklist and venue length/layout requirements.
- Keep ethics, funding, conflicts, data/code availability and author information
  accurate; label missing statements instead of fabricating them.
- Reopen/compile the saved artifact when the format requires it. State which checks
  ran, what remains unverified and where the files were saved.
- For reviewer responses, map every comment to a change and its exact location;
  explain scientifically justified disagreements respectfully. Formal independent
  peer review is a separate task, not a label for this self-check.
