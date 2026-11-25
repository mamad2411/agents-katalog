---
name: create-professional-proposals
description: Create premium, client-ready business proposal PDFs from raw, incomplete, or finalized content. Use for commercial proposals, project proposals, service offers, technical proposals, partnership proposals, sponsorship proposals, agency proposals, and similar documents in Arabic, English, or bilingual Arabic-English. Improve structure and wording, apply supplied branding or create a suitable visual direction, generate the PDF, and verify both content and rendered layout before delivery.
---

# Create Professional Proposals

Create an intentional business document, not a decorated text export. Make the proposal persuasive, easy to scan, commercially precise, and visually coherent with the client's context.

## Required companion workflow

Read and follow the built-in `pdf` skill completely before creating or editing the PDF. Use its output conventions, rendering workflow, and visual verification requirements. If that skill is unavailable, reproduce its core standard: create the PDF programmatically, inspect extracted text, render every page to images, inspect the images, correct defects, and repeat until clean.

Read the bundled references as follows:

- Read `references/content-architecture.md` before drafting or restructuring.
- Read `references/design-system.md` before choosing layout, typography, colors, or page composition.
- Read `references/bilingual-layout.md` for any Arabic or bilingual proposal.
- Read `references/quality-gates.md` before final verification and delivery.

## Operating principles

- Preserve every supplied fact, name, price, percentage, date, scope item, exclusion, timeline, legal term, and commercial condition.
- Improve organization, grammar, clarity, tone, headings, transitions, and concision by default.
- Never invent missing business facts. Mark unresolved items clearly and ask only when they materially affect accuracy or design.
- Treat the user's latest explicit instructions as authoritative when source content conflicts.
- Avoid overstating guarantees, capabilities, outcomes, or commitments.
- Match the proposal's sophistication to its audience and deal size; avoid generic corporate filler.
- Use supplied brand assets faithfully. Never redraw or alter a logo unless explicitly requested.

## Workflow

### 1. Build the content brief

Identify the proposal's language, audience, sender, objective, services or deliverables, commercial model, timeline, terms, call to action, and available branding. Infer only low-risk presentation choices.

Ask focused questions only for blocking omissions. If the user wants immediate execution, proceed with explicit neutral labels such as `To be confirmed` / `يُحدد لاحقًا` rather than fabricating values.

### 2. Audit and normalize the source

Create a private fact ledger containing all critical names, figures, dates, deliverables, exclusions, and terms. Resolve obvious spelling and grammar issues without changing meaning. Surface contradictions before finalization.

### 3. Shape the proposal narrative

Use `references/content-architecture.md`. Select only sections that strengthen the proposal. Remove repetition and empty claims. Use specific, benefit-led language grounded in the supplied content.

For material wording changes, keep the commercial meaning identical. Preserve quotations or approved contractual language verbatim when the user marks it as fixed.

### 4. Select the visual direction

If branding is supplied, derive colors, typography, and graphic treatment from it. If it is incomplete, extend it conservatively. If no branding is supplied, create a restrained visual system appropriate to the sector, audience, and proposal tone using `references/design-system.md`.

Do not ask the user to choose among arbitrary styles unless the choice would materially change the outcome.

### 5. Compose the document

Prefer A4 portrait unless content or user intent strongly favors another format. Use reusable page primitives for cover, section opener, standard content, cards, tables, timeline, pricing, terms, and closing page. Keep grids, spacing, header/footer behavior, page numbers, and section rhythm consistent.

Use real vector shapes, text, and high-resolution imagery. Do not rasterize the entire document. Keep body text selectable and searchable.

For Arabic or bilingual work, follow `references/bilingual-layout.md` exactly. Verify that the selected font includes Arabic glyphs and that shaping, ordering, punctuation, numbers, and alignment render correctly.

### 6. Generate and verify

Generate the PDF with the most reliable available toolchain. Prefer the workspace's supported PDF runtime and deterministic layout code. Keep temporary render files outside the final output directory.

Run `scripts/inspect_proposal_pdf.py FINAL.pdf` for structural checks. Then render every page to PNG and inspect every page visually. Use a contact sheet only for overview; inspect full-size pages for dense tables, Arabic text, pricing, and terms.

Compare extracted critical facts against the private fact ledger. Correct all issues and rerun both structural and visual checks.

### 7. Deliver

Deliver the final PDF with a clear filename and a concise summary. Mention unresolved placeholders or assumptions, if any. Do not deliver debug files, rendered PNGs, or temporary sources unless requested.

## Non-negotiable quality bar

- No clipped, overlapping, overflowing, missing, or corrupted text.
- No broken Arabic shaping, reversed text, disconnected letters, or mixed-direction punctuation errors.
- No widows, orphaned headings, nearly empty pages, accidental blank pages, or split table rows where avoidable.
- No inconsistent currencies, totals, dates, terminology, capitalization, or numbering.
- No stock-template feel, excessive decoration, low-contrast text, tiny type, or unexplained icons.
- No unsupported factual claims or silent commercial changes.
- Do not claim completion until the latest rendered pages pass visual inspection.
