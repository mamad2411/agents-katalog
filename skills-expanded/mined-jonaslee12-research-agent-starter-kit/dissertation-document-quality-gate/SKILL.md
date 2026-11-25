---
name: dissertation-document-quality-gate
description: Review formal research outputs before delivery, including proposal drafts, ethics/compliance materials, Word documents, source notes, reports, manuscripts, and stakeholder-facing summaries, using success criteria, evidence checks, formatting/render checks, and unresolved-field reporting.
---

# Research Document Quality Gate

Use this skill before delivering or finalising formal research documents, especially Word files, proposal sections, ethics/compliance materials, participant-facing documents, supervisor/PI/client/reviewer summaries, source registers, reports, manuscripts, and literature review drafts.

## Purpose

Adapt eval-harness, verification-loop, and checkpoint practices to research-project work. Define success criteria, inspect the output against them, fix issues, then report remaining risks.

## Gate Levels

Use the lightest gate that fits the risk.

| Level | Use When | Required Checks |
|---|---|---|
| Light | chat answer, small note, quick summary | answer matches request, no obvious invented facts, open questions marked |
| Standard | project wiki, Obsidian note, source register, planning document | source paths present, evidence boundary clear, links/files exist, no raw sensitive data |
| Formal | proposal, ethics form, participant-facing material, manuscript, report, grant, supervisor/PI/client/reviewer-facing Word/PDF | source-first gate passed, facts verified, citations checked, project delivery review completed, formatting/render checked, `TO CONFIRM` fields listed |

## Success Criteria

Before checking, state or infer:

- intended audience
- purpose of the document
- required format
- source files used
- must-have sections
- facts that must be exact
- risks to avoid

## Required Checks

### Evidence

- confirmed facts have source paths or URLs
- interpretations are labelled
- citations are verified enough for the claim
- contextual sources are not treated as empirical evidence
- no fabricated participant, supervisor, institutional, or personal details

### Research Logic

- research focus is visible
- gap/problem statement is connected to the selected project profile and evidence base
- methodology or workflow matches current project stage
- expected contribution does not overclaim beyond what the evidence and method can support
- for major planning or revision outputs, the section rationale matrix, revision matrix, or logic-transfer audit exists when needed

### Requirement / Delivery Readiness

For formal, supervisor-facing, or submission-facing outputs:

- apply `quality-gates/PROJECT_DELIVERY_REVIEW_GATE.md` before delivery
- apply `university-guidance/RUBRIC_EVIDENCE_GATE.md` before any assessed academic grade-band or marking-criteria judgement
- apply `university-guidance/DISTINCTION_DELIVERY_REVIEW_GATE.md` only when assessed academic high-band readiness is relevant
- state the requirement evidence level: official original text, local summary, inference from local summary, or evidence insufficient
- produce an indicative readiness statement rather than an official mark, acceptance decision, funding decision, approval, or client sign-off
- revise feasible weaknesses before delivery, then re-check the revised version
- do not call a document submission/client-ready while required ethics, compliance, source, format, word-count, appendix, AI declaration, or referencing details remain unresolved

### Language And Style

- use `uk-academic-writing-style` for proposal, literature review, methodology, supervisor/PI/client/reviewer-facing, or academic prose when relevant
- use `style-memory-and-revision-gate` for major chat answers, revised documents, and supervisor-facing summaries
- recommendation or section purpose appears before extended reasoning
- British English is used where appropriate, unless preserving source titles, template wording, or citation metadata
- generic AI-style phrasing is removed without weakening evidence boundaries
- for generated Markdown-to-Word outputs, scan the source Markdown or extracted document text for the user's prohibited style patterns before rendering or delivery
- if a bilingual or Chinese explanation section is included, check the Chinese text as seriously as the English academic prose

### Ethics And Privacy

- no raw participant data in general notes
- participant-facing documents avoid unnecessary personal disclosure
- recruitment, consent, withdrawal, data retention, and AI-use claims are source-grounded
- teacher evaluation, surveillance, and student-data risks are bounded

### Word / Formatting

For important `.docx` outputs:

- check project-specific format requirements when they exist
- follow current official project, journal, funder, client, university, or institutional requirements over generic public formatting guidance when they conflict
- preserve original file unless overwrite is requested
- generate a clearly named revised file
- when a Markdown source is rendered to Word, run `scripts/markdown_docx_structure_check.py` or rely on `scripts/formal_delivery_guard.py` with the Markdown source so tables and structural features are not silently flattened
- run `scripts/docx_layout_review_check.py` for important Word outputs, and pass `--previous-docx` when revising a previously accepted Word document
- render to PDF/PNG when possible
- inspect key pages for broken numbering, clipped text, awkward page breaks, and formatting errors
- record a layout self-review verdict; unresolved table loss, heading flattening, or unexplained regression is delivery-blocking unless the user explicitly accepts an override risk
- use `TMPDIR=/private/tmp` for document rendering on macOS

### Visible Output QA

For Word/PDF, figure, diagram, browser, Obsidian, GitHub, or other user-visible deliverables, use `research-wiki/VISIBLE_OUTPUT_QA_PROTOCOL.md`.

Record:

- artifact;
- communication job;
- rendered output or preview path;
- deterministic checks;
- visual inspection;
- baseline/regression check;
- unresolved risks;
- delivery verdict.

When local tools are available, validate the note:

```bash
python3 scripts/visible_output_qa_check.py <qa-note.md>
```

A Visible Output QA pass only proves that the visible surface was checked. It does not prove citation support, compliance readiness, academic/professional quality, or submission readiness.

### Artifact Completeness

For important proposal, chapter, manuscript, report, stakeholder-facing, or revision-package outputs, check whether the task needs:

- source map,
- working or confirmed motivation,
- motivation thread model,
- section blueprint,
- section rationale matrix,
- revision matrix,
- logic-transfer audit,
- citation/source status,
- `TO CONFIRM` list,
- Word/render check.

Use `../dissertation-argument-spine/references/paperspine-adapted-writing-controls.md` for the adapted PaperSpine completeness table. Missing artifacts are acceptable for small tasks only when the final report explains why they were not needed.

## Verification Loop

1. Check against success criteria.
2. Fix concrete issues.
3. Re-check only the affected areas.
4. Record residual risks and `TO CONFIRM`.

Do not keep polishing if the document already satisfies the task and remaining changes are taste-level.

## Final Report Shape

For document work, final answer must state:

- what changed
- why it changed
- new file path
- verification performed
- project delivery review evidence level and post-revision readiness status
- what still needs user confirmation

Use concise Chinese unless the document itself is in English.
