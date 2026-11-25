---
name: social-science-submission-packager
description: Use when a social-science paper project needs a submission-ready package, especially with manuscript, figures, tables, citations, reviewer comments, data/code notes, reproducibility materials, and final freeze checks.
---

# Social Science Submission Packager

Use this skill when the target is a submission package, revision package, final manuscript freeze, reproducibility bundle, or paper delivery bundle. It is the controller for package-level readiness; it does not replace citation verification, paper review, figure design, writing export, or reproducibility checks.

## Required Contracts

Before packaging, read:

- `<VELA_RUNTIME_ROOT>/skills/catalog/peer_review_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/publication_style_rules.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/quality_gates.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/research_pipeline_stages.json`

Use `submission_package_review` mode in `peer_review_workflow.json`.

## Scope

This skill coordinates:

- manuscript version and target venue
- figures and tables
- references and citation evidence
- reviewer comments and response package
- data/code/material availability
- reproducibility package
- internal/private vs public delivery boundary
- final freeze decision

It does not directly write the final manuscript unless the user explicitly authorizes writing edits through the writing route.

## Venue Migration And Resubmission

Use this package controller when the user asks to:

- change conference or journal;
- 改投别家、换会议、换期刊、转投、重投;
- migrate between LaTeX or Word templates;
- prepare a revise-and-resubmit or resubmission package;
- check whether a manuscript is ready for a different venue.

This is a package-level task, not just a formatting task.

Before changing files, create a target-requirement checklist:

- current venue/format and target venue/journal;
- official author instructions or template source;
- page, word, figure, table, reference, appendix, and supplementary limits;
- anonymity, ethics, data/code availability, funding, conflict-of-interest, checklist, and disclosure requirements;
- required manuscript sections and forbidden/optional sections;
- figure/table format, resolution, caption, and source-data requirements;
- citation style and bibliography requirements;
- whether the task is mechanical migration, substantive rewriting, or both.

Then separate work into:

- mechanical migration: template, class file, headings, metadata, figure/table placement, bibliography style, checklist files;
- substantive adaptation: introduction framing, theory/literature positioning, method transparency, limitations, data/code statement, response to likely target-venue expectations;
- unresolved blockers: missing official instructions, missing source manuscript, missing figures/tables, unresolved citation evidence, missing data/code availability, or target-specific ethics requirements.

Do not mark a migration ready until the applicable citation, writing, peer-review, figure-table, reproducibility, and final-freeze gates are satisfied.

## Workflow

1. Lock package boundary:
   - project root
   - manuscript version
   - target venue or submission context
   - public/internal files
   - raw/private materials that must not be exported
2. Confirm required gates:
   - `doi_and_metadata_verified`
   - `writing_quality_checked`
   - `peer_review_protocol_checked`
   - `figure_table_consistency_checked`
   - `reproducibility_bundle_verified`
   - `final_package_frozen`
3. Delegate subchains:
   - citation and writing-use references -> `writing-reference-capture`
   - single paper or internal review -> `academic-paper-review`
   - reviewer response -> `reviewer-response-pack`
   - figures/tables -> `research-figure-studio` or `figure-table-studio`
   - data/code bundle -> `reproducibility-package`
   - Word/LaTeX export -> `research-docx-export` or `latex-paper-conversion`
4. Build `submission_review_manifest`:
   - manuscript version
   - citation report
   - writing quality report
   - peer review report
   - figure/table report
   - reproducibility report
   - package boundary
   - freeze decision
5. If any gate is missing or not pass, do not call the package ready. Return a blocker list.

## Writing Quality Freeze

Before freezing the manuscript, verify the writing-quality report covers the direct-argument rules:

- the manuscript can be summarized in four sentences: background, problem, method or materials, finding;
- the contribution is stated before limits and is not weakened beyond the evidence;
- defensive openings, negative setup formulas, mechanical transitions, AI-like phrasing, translationese, internal workflow terms, and self-coined terms have been removed or justified;
- Chinese concepts follow Chinese-language scholarship and established Chinese academic usage;
- paragraphs and sentences vary naturally with the argument instead of forming uniform short blocks.

If this check fails, return to `manuscript-writing-studio` or `academic-humanization-studio` before package freeze.

## Output Contract

```markdown
# Social Science Submission Package

## Package Boundary

## Required Gates
| Gate | Status | Evidence path | Blocker |
|---|---|---|---|

## Delegated Subchains

## Submission Review Manifest

## Freeze Decision
- ready_to_submit
- revise_before_submit
- blocked

## Blocker List

## Next Actions
```

## Red Lines

- Do not freeze a package with unresolved citation, peer-review, figure/table, writing, or reproducibility gates.
- Do not expose private paths, raw data, credentials, Zotero database internals, browser state, or restricted PDFs in public deliverables.
- Do not treat an AI review score as venue acceptance.
- Do not let a reviewer directly rewrite the main manuscript or overwrite data/code.
