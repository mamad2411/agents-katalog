---
name: ingest
description: Digest a source document into Knowledge — reports, protocols, scope records, presentations, meeting notes, and published material. Use when the user shares or points to a document and wants it read, summarized, absorbed, or added to project knowledge.
disable-model-invocation: true
---

# familiar — Ingest a Source

**Authoritative pipeline: `.familiar/core/ingest.md`. Read it before ingesting.**

## Context contract

- **Required context:** `.familiar/core/voice.md`, `.familiar/core/plain-language.md`, `.familiar/core/file-handling.md`, the one source named, and `3-Knowledge/_knowledge-index.md`
- **Conditional context:** the active extraction capability for the source format, and an existing page only when reconciling the same source.
- **Excluded context:** Other projects, undeclared extension content, and project areas not required or conditionally triggered here.
- **Updates:** one page in `3-Knowledge/` plus its index row and its `3-Knowledge/_source-register.md`
  row (and `3-Knowledge/_abbreviations.md` when the source introduces a new term); in a check pass, the
  checked pages' agreed corrections and `values_checked` stamps, and their index rows; `5-System/Memory/status-log.md`, but only for a material ingest event. Never
  `Inputs`
- **Capabilities:** file-read, file-write. Optional capabilities must degrade as the procedure states.
- **Completion:** Read mode returns a locator-grounded answer without writes; ingest mode creates one provenance-complete page — which REQUIRES a stamped `ref_carry_through` per `ingest.md` step 5; a page missing that field is not complete, regardless of how the synthesis reads — and one matching index entry, with conflicts, extraction limits, and a low ref-carry-through reported.


## Step 1 — Choose the mode

`ingest.md` → Read mode or ingest mode defines them. This skill is user-only, so the user started it: ingest mode. Run
the pipeline; do not ask whether the source is worth keeping. When the user asked only what the source says: read mode.
Answer, write nothing, and offer a full ingest if the source looks like durable project knowledge.

## Step 2 — Full ingest pipeline (only if warranted)

1. Confirm the raw source sits in `Inputs` (read-only — never edit it).
2. Run the pipeline steps in `ingest.md` → Ingest procedure. For meeting notes, minutes, or a
   transcript (typically `1-Inputs/Sources/Meetings/`), follow `ingest.md` → Meeting notes as well.
   Between extraction and synthesis, apply `ingest.md` → Size check. It warns once on a
   multi-source or oversized request and offers one source per fresh context. If the user runs
   them all, follow `ingest.md` → Bulk ingest.
   When the user asks to check pages against their sources, or a bulk ingest finishes, follow
   `ingest.md` → Check pass. It compares and reports first, and changes a page only on a yes.
3. Write a **by-source** synthesis page into `3-Knowledge/` — pages are organized by source,
   not by topic.
4. **Citations are mandatory in both modes**, with locators. No uncited claims. Where the source
   carries its own citation marker (numbered ref, footnote, superscript, or inline author-date),
   carrying it through is not optional and is not a later cleanup pass — `ingest.md` → Ingest
   procedure step 4 governs, and must be satisfied before this page is considered written, not
   after.
5. Update `3-Knowledge/_knowledge-index.md`.
6. Add cross-links per the "Cross-links" section.

## PDFs — use the active extraction capability

**Where the scripts are.** This skill's scripts sit in its own `scripts/` folder. Commands below
give the Claude Code path, run from the project root; on Codex and Gemini put `.agents/` where
they say `.claude/`.

Run `.claude/skills/ingest/scripts/extract_pdf.py --health-check` before touching a PDF for the first time
in a session. If it reports `"extract": false`, report the missing dependency and stop rather than
running the extraction and hitting an import error mid-task. Otherwise run
`.claude/skills/ingest/scripts/extract_pdf.py` (see its module docstring for `--ocr`/`--pages` options)
and preserve its page locators; write the output to `3-Knowledge/_extract-<stable-source-ID>.md` per
`ingest.md` → Ingest procedure step 2. If no validated capability is active, report the source as
unavailable rather than page-by-page guessing. Never send a confidential or restricted PDF to a
hosted parser without explicit approval. Full host-neutral policy: `.familiar/core/ingest.md`.

## Source register — before and after

Start every full ingest with `.claude/skills/ingest/scripts/source_register.py scan` and show the user the
receipt; finish it with `source_register.py record`, per `ingest.md` → Ingest procedure steps 1
and 9. That is what stops a renamed copy being synthesized twice, and lets an interrupted ingest
resume instead of restarting.

## Word documents — EndNote citations

For every `.docx` source, run `.claude/skills/ingest/scripts/extract_encite.py` per `ingest.md` → Ingest
procedure step 2 before synthesizing. It is stdlib-only and reads nothing but the source. Its
records tell you which study each numbered marker cites; use them when carrying markers in step 4.
If it cannot run, say so and carry markers from the rendered text.

## Step 3 — Report

Tell the user which mode you used, what you wrote, and where, including the `ref_count.py` line for the
page (`ingest.md` → Ingest procedure step 5). If the source contradicts an existing knowledge
page, **flag the conflict** — do not silently overwrite or reconcile it. If the page's
`ref_carry_through` count looks low against how densely the source itself cites, say so — this is
the moment to fix it, before a later drafting skill goes looking for a primary source that never
made it into the page.

## Guardrails

- `Inputs` is **read-only**. Writes go only to `Knowledge` and the declared `5-System/Memory/status-log.md` memory
  update above — nowhere else.
- Never fabricate a citation or a locator. If you cannot locate a claim, say so.
- Office files are ZIP archives — verify integrity before reading (`file-handling.md` → Integrity and delivery).
- If several by-source pages start circling one theme, propose a **topic page** rather than creating one unasked.
