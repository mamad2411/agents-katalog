---
name: cdd-assess
description: Create source-grounded CDD onboarding assessment reports from client materials. Use when compliance teams need evidence bundles, regulatory grounding, and versioned HTML reports.
---

# CDD Assess

Use this skill to own the workflow from onboarding materials to a polished internal HTML CDD assessment report. The report records facts first, then assessment observations. It must not recommend approval, rejection, escalation, conditions, or operational actions.

Never trust parametric knowledge for regulatory requirements. Use supplied compliance materials first; when they are missing, stale, or insufficient, research official primary or high-trust sources and persist the findings before drafting.

## Bundled Resources

- `assets/report-template.html`: default professional HTML report shell; adapt structure and labels to user feedback and case needs.
- `assets/report.css`: print-friendly report styling with stable typography, numeric alignment, and evidence-image treatment.
- `assets/logo-placeholder.svg`: replace with the firm's logo.
- `assets/watermark-placeholder.svg`: replace with the firm's watermark.
- `references/cdd-concepts.md`: self-contained portable CDD methodology for customer understanding.
- `references/completeness-checklists.md`: mandatory coverage checks for individual and corporate reports.
- `references/report-composition.md`: narrative report-writing standard and observation-card format.
- `references/workspace-format.md`: case workspace and review bundle layout.
- `references/operating-context-onboarding.md`: first-run concierge intake for empty or incomplete workspaces.
- `references/principles.md`: mission, philosophy, and report judgment principles.
- `references/research-finding-format.md`: persisted regulatory research format.
- `references/report-rendering.md`: HTML rendering and quality checks.

Read the relevant reference only when performing that part of the workflow.

## Mission

Turn messy onboarding materials into a review-grade factual record: sourced, structured, visually clear, and humble about uncertainty, so a human compliance reviewer can understand the client without reconstructing the work.

## Philosophy

- **Facts before assessment**: record what is known, where it came from, and how reliable it is before making observations.
- **No silent certainty**: mark estimates, weak extraction, conflicts, and missing evidence visibly.
- **Customer understanding is the spine**: individual and corporate clients need different factual records and derivations.
- **Narrative carries judgment**: tables preserve auditability, but prose explains the customer, evidence, uncertainty, and regulatory relevance.
- **Derivations must be inspectable**: SOW, SOF, net worth, and UBO maps must show inputs, assumptions, method, and confidence.
- **Primary sources over memory**: when compliance grounding is missing or stale, research official sources and persist reusable findings.
- **Beauty serves judgment**: layout, tables, charts, screenshots, and citations exist to reduce reviewer effort.
- **Human authority stays outside the report**: the report supports review; it does not recommend decisions or actions.

## Workflow

### 1. Establish Operating Context

Before drafting any report, confirm the workspace has an operating context. If `OPERATING_CONTEXT.md` is missing, blank, stale, or visibly incomplete, read `references/operating-context-onboarding.md` and run the concierge intake: create a draft context file, inspect local files before asking, ask one focused blocking question at a time, and save each answer immediately. If the officer provides a completed context file, ingest it and ask only about gaps or conflicts.

Minimum context:

- compliance officer name, role, team, and represented entity
- jurisdiction(s), regulator(s), and source freshness policy
- client types handled: individual, corporate, trust, fund, intermediary, other
- internal policies, procedures, checklists, risk methodology, and report expectations
- report audience, confidentiality level, logo, watermark, and style requirements
- available compliance knowledge pack and known gaps

You may create the workspace, inventory materials, and propose grouping before the context is complete. Do not draft an assessment report before the report-critical context exists. Do not ask a long setup questionnaire in one message unless the user explicitly requests a form.

### 2. Create Or Reuse Case Workspace

Use a stateful workspace. Read `references/workspace-format.md` before creating or changing the structure.

Preserve the original source drop untouched. If materials are mixed across multiple clients, infer a grouping plan using folder names, filenames, extracted names, registration numbers, form types, and document text. Ask for confirmation before copying materials into normalized client packs. Put ambiguous files in `unassigned/`.

For each confirmed client pack, identify the customer type before analysis: `individual`, `corporate`, or `unclear`. Ground individual clients under the individual factual record and corporate clients under the corporate factual record. If the type is unclear, block report drafting for that client pack until the ambiguity is resolved.

### 3. Ground The Review

Build or refresh the compliance knowledge base for this case.

Source hierarchy:

1. user-supplied entity policies, procedures, checklists, and risk methodology
2. official regulator, statute, FIU, government, court, or supervisory sources
3. recognized standards bodies such as FATF, Wolfsberg, Basel, IOSCO, or similar
4. secondary sources only for orientation, never final authority

If grounding is missing or stale, browse primary/high-trust sources. Persist each reusable finding using `references/research-finding-format.md`: requirement, citation, access date, interpretation, rationale, practical report implications, uncertainty, and jurisdiction limits.

If no adequate authority can be found, state the gap. Do not convert unsupported recall into an observation.

### 4. Run Specialist Passes

Use subagents when the runtime supports them; otherwise run the same passes sequentially. Keep raw pass outputs in the review bundle.

Required passes:

- **Extraction pass**: extract text, tables, screenshots, and page references from materials, down to transaction lines, register rows, and MRZ lines.
- **Factual record pass**: classify customer type, then structure identity, entity, ownership, financial, document, and transaction facts under the individual or corporate record.
- **Regulatory research pass**: ground applicable requirements and principles.
- **Derivation pass**: derive SOF, SOW, net worth corroboration, UBO maps, conflicts, and estimates, with quantified coverage of declared versus independently evidenced amounts. For corporate ownership, document every intermediate entity and natural person down each ownership layer with per-layer evidence status.
- **Arithmetic verification pass**: mechanically recompute every numeric claim that will appear in the report: totals, residuals, coverage ratios, FX conversions, ownership percentages, expected-activity arithmetic, source counts, conflict/gap counts, and key-figures metrics. Save the script output or table in `review-bundle/arithmetic-check.md`.
- **Consistency sweep**: cross-check every extracted value across documents (names and MRZ order, identifiers, dates, addresses, contact details, values, tenures) and record each check and anomaly per `references/report-composition.md`.
- **Completeness pass**: apply `references/completeness-checklists.md`; include mandatory rows even when facts are `not observed`.
- **Citation review pass**: verify every material fact and observation cites document plus page/section plus field or line, extraction method, and confidence.
- **Narrative composition pass**: read `references/report-composition.md` and compose analytical prose that climbs the corroboration ladder for every material claim.
- **Report critique pass**: check completeness, clarity, visual usefulness, print-stable presentation, and no decision/action language.

For every extracted or derived item, record source file, page/section, method, confidence, assumptions, and reviewer status. Low-confidence OCR/table parsing or ambiguous derivation is `Needs human verification`, not a confirmed fact.

### 5. Produce Review Bundle

Before rendering HTML, produce a review bundle containing:

- material inventory and grouping plan
- operating context and source freshness status
- extracted facts with citations and confidence
- derivations with inputs, method, assumptions, and confidence
- evidence index for screenshots, tables, charts, and document snippets
- research findings and applicable principles
- completeness checklist with mandatory coverage rows
- arithmetic check with every report figure recomputed
- narrative composition notes: customer story, evidence strength, conflicts, and observation cards
- conflicts, missing facts, and human-verification items
- report outline and review-pass notes

Resolve contradictions explicitly. Do not hide conflicting source evidence.

If no visual evidence artifact is generated for a critical exhibit, record `No visual evidence generated` as a gap with the reason. Every absence claim must state where the analyst looked. Preserve raw specialist pass outputs as separate files or clearly marked sections; do not keep only the synthesized report.

### 6. Render Versioned HTML Report

Read `references/report-rendering.md` and `references/report-composition.md`, copy the bundled template/CSS into the workspace, and render a versioned report whose filename includes version, customer type, and short customer name, such as `reports/v001-individual-jane-tan-onboarding-assessment.html` or `reports/v001-corporate-acme-pte-ltd-onboarding-assessment.html`.

The bundled HTML structure is a starting point, not a fixed schema. Adapt section order, labels, exhibits, page breaks, and layout when user feedback, case materials, or reviewer needs justify it, while preserving mandatory coverage, sourceability, page numbering, render checks, and no decision/action language.

Default adaptable report structure:

1. compact dossier header: logo, watermark, confidentiality, version, preparer, reviewer context; then table of contents
2. reviewer brief: key-figures band, customer story, main evidence strengths, main uncertainties
3. evidence map: source inventory, reliability, extraction method, confidence, freshness
4. customer understanding: identity/legal existence, relationship purpose, expected activity
5. client-type analysis: SOW, SOF, net worth, UBO/ownership/control, plausibility, conflicts
6. evidence exhibits: numbered figures, exhibit register, screenshots, charts, document snippets with captions
7. regulatory grounding: applicable requirements, principles, source freshness
8. assessment observations: criterion, observed condition, evidence, review significance, limits
9. gaps, human-verification items, review comments
10. version history, appendix fact tables, and mandatory disclaimer

Focus most effort on sections 4 and 5. The body must be readable as prose before the reviewer inspects tables, and the analysis must reach triangulation and quantified residual uncertainty per `references/report-composition.md`. Use figures, ownership diagrams, cited exhibits, and compact appendices to support the narrative, not replace it.

### 7. Final Self-Check

Before delivery, verify:

- original source drop is preserved
- operating context exists
- regulatory grounding is source-backed and fresh enough
- every material fact cites document plus page/section plus field or line, with extraction/derivation confidence
- each major section opens with a sourced narrative summary and names its main uncertainty
- corroboration statements are quantified: declared amount, evidenced amount, remainder
- every numeric claim in the report ties to `review-bundle/arithmetic-check.md`
- the consistency sweep is recorded and every anomaly appears in the report
- every `not observed`, `not provided`, or `not performed` claim includes a search trail
- conflicts and gaps are ordered by factual materiality and include amount-at-stake or affected analysis
- corporate ownership maps document every intermediate entity down to natural persons with per-layer evidence status
- analytical body sentences are about the customer, documents, and facts — not about the report itself
- mandatory coverage rows are present for PEP/RCA, sanctions/adverse media, tax residency, expected activity, document freshness/expiry, and official-source freshness
- estimates show method, assumptions, and uncertainty
- screenshots/exhibits cite their source
- the rendered PDF passed the render check in `references/report-rendering.md`; watermark does not obstruct text; headings are meaningful and wrap cleanly; figures, numeric columns, and evidence images remain readable; color is not the only status signal
- review comments and version history are present
- report is marked internal compliance use only
- report contains no approval, decline, escalation, condition, next-action, or recommendation language
- disclaimer is present:

> Drafted by an AI assistant for review by a qualified compliance professional. Not a regulatory determination, approval, recommendation, or instruction.

If any check fails, revise the bundle/report or clearly mark the unresolved issue for human verification.
