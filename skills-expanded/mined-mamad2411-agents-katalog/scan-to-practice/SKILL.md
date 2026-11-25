---
name: scan-to-practice
description: A complete methodology for turning scanned or image-based learning materials into high-quality desktop, web, or mobile practice products. Covers visual transcription, data assembly, answer-key-driven controls and grading, product design, animation, validation, and long-term maintenance. Use when a user wants to convert scanned exercises, workbook pages, or question-bank photos into an interactive practice application, including typed answer controls, persistent attempts, and mistake review.
---

# Scan-to-Practice: Scanned Materials to Practice Product

## When to use this skill

- The user has scanned PDFs, workbook pages, or question-bank photos and wants an interactive text-based practice product.
- The product needs daily plans, progressive difficulty, progress tracking, mistake review, and multilingual explanations.
- Verified answer records need to become in-place choice, true/false, numeral, or free-text practice controls.
- The user wants to evaluate feasibility, architecture, cost, or quality controls before implementation.

## Core principles

1. **Source fidelity over AI invention.** Questions and official answers must come from authorized source material. Clearly label generated examples as synthetic or unofficial.
2. **Fix data before presentation.** Correct transcription and structural problems in source data after making a backup. Keep rendering logic focused on presentation.
3. **Validate the complete dataset.** Sampling is useful for progress reports, not for final conclusions. A script finishing successfully does not prove content correctness.
4. **Confirm consequential decisions.** Ask the user to approve transcription scope, answer format, information architecture, and directory structure before large-scale work.
5. **Clarify visual or animation changes.** Users may strongly value distinctive interactions; confirm the intended behavior before replacing or removing them.

## Nine-stage pipeline

```text
1. Rights and source audit
2. Library design: structure, difficulty, and schedule
3. Visual transcription: image to text
4. Data assembly and validation
5. Self-contained content format
6. Application architecture
7. Visual system
8. Animation and assets
9. Packaging, verification, and maintenance
```

Detailed references:

- `docs/01-project-journey.md` — the complete delivery journey and implementation sequence
- `docs/02-troubleshooting.md` — failure modes organized as symptom, root cause, fix, and verification
- `docs/03-methodology.md` — the reusable pipeline, design system, cost model, and tool checklist
- `docs/04-answer-interaction.md` — answer-key-driven controls, grading state, failure handling, and coverage verification; read this when implementing answer entry or grading

## Quick decision card

| Question | Recommended approach |
|---|---|
| Does the PDF contain a text layer? | Test a representative page with PyMuPDF `get_text()`. An empty result usually means visual transcription is required. |
| Which transcription engine? | Benchmark a capable paid vision model on representative pages. Conventional OCR may fail on dense tables, answer lines, italics, and complex layouts. |
| What should the prompt require? | Complete transcription; preserve numbering, blank lines, and tables; output source text only; do not explain or translate. |
| How should cost be estimated? | Measure tokens, latency, and retry rates on a small sample, then extrapolate. A reference run of 2,584 pages used about 7.3M tokens, CNY 23–42, and 8–12 background hours. |
| What are the major risks? | Reasoning tokens consuming the output budget, two-dimensional layouts collapsing, long documents being truncated, and segmentation based on ordinary body words. |
| How should difficulty be assigned? | Combine domain consensus, published statistics, task cognitive load, and later calibration from user accuracy. |
| Which desktop stack? | Electron is practical for a rich local interface. Use either simple native JavaScript or a modern React-based stack according to team size. |
| How should answer controls be generated? | Parse verified answers by question number, classify the response type, extract options from the same question range, and attach controls only to matching rendered anchors. Report gaps instead of fabricating structure. |
| What visual direction worked? | A restrained paper-inspired theme, low-chroma OKLCH colors, consistent spacing, and deliberate easing such as `cubic-bezier(0.16,1,0.3,1)`. |
| How should validation work? | Layer syntax checks, full-dataset smoke tests, source-consistency assertions, answer-control coverage from production functions, browser-level interaction tests, and screenshot review. |
| What follows a source-data change? | Synchronize every runtime copy, rebuild indexes, and rerun the full verification suite. |

## Validated implementation notes

- Visual transcription averaged roughly 10–13 seconds per page in the reference project.
- Disable unnecessary model reasoning when the provider supports it; otherwise reasoning may consume the output budget and return empty transcription.
- Write each completed page to disk immediately and support resumable processing.
- Use structure anchors such as `SECTION`, `READING PASSAGE N`, and `WRITING TASK N`; never classify a page from ordinary body-text keywords.
- Reconstruct maps and plans programmatically from measured row and column anchors rather than manually counting spaces.
- Subset large fonts with `pyftsubset`, then verify every required character.
- Use lossless image compression such as `oxipng` for distributable assets.
- Extract the actual rendering functions for assertions so test logic cannot silently drift away from production behavior.
- Treat the rendered exercise as the visual source of truth and the verified answer key as grading semantics; never create a control for an answer record without a matching question anchor.
- Classify true/false, yes/no, letter, multiple-letter, Roman-numeral, and free-text answers before rendering controls.
- Key persisted attempts by practice ID, section, and question number, and update only the affected control and mistake summary after grading.
- Normalize free-text answers conservatively and test both accepted variants and near-miss negatives.
- Keep animation frames limited to `transform` and `opacity` whenever possible.

## Common traps

- Markdown table column mismatches can drop cells or prevent table parsing; normalize columns before rendering.
- Long underscore sequences may be interpreted as emphasis; use escaped entities or CSS borders for answer lines.
- An unclosed `<details>` element can swallow the rest of the document; assert matching opening and closing counts.
- CSS `display` rules can override the HTML `hidden` attribute; add explicit `[hidden]{display:none}` rules where required.
- Full-width spaces can break tables, while normal spaces may be essential for diagrams; normalize them separately.
- A global regular expression reused with `test()` carries `lastIndex` state and can skip lines.
- A `Questions N-M` range heading is context, not an answerable row; broad number matching can attach controls to the wrong element.
- Global option extraction can borrow labels from an unrelated question range, while broad fuzzy matching can mark a wrong free-text answer as correct.
- Batch success counts prove execution, not content quality; inspect boundaries, compare backups, and run content-level assertions.
- Validate the validators against known-good and known-bad fixtures.

## Maintenance protocol

When a new failure pattern appears:

1. Reproduce it on a concrete source fragment.
2. Decide whether it belongs to data, rendering, interaction, or environment.
3. Implement a general rule rather than a one-file patch.
4. Measure the full-dataset impact.
5. Run targeted checks and the full regression suite.
6. Record the new pattern in `docs/02-troubleshooting.md` or the appropriate reference.
