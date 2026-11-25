---
name: source-analysis
description: Analyze one raw source file and write a structured `.cache/source-id-analysis.md` handoff document for `wiki-generation`.
---

# Source Analysis

This skill analyzes exactly one source file and writes one handoff document under `.cache/`.
Do not generate formal wiki notes here.
Do not decide final argument insertion order here.

## Read First

- `references/output-schema.md`

Search existing notes when needed for duplicate, update, or placement judgment:
- `wiki/permanent-notes/`
- `wiki/argument-notes/`
- `wiki/structure-notes/`
- `wiki/reference-notes/`

## Input And Output

- Input: one source file, usually from `raw/`
- Output: `.cache/<source-id>-analysis.md`
- `source-id` = source filename without extension

## Workflow

1. Fix the active unit.
   Work on exactly one source file. Prefer the next pending file under `raw/` unless the user names another file.

2. Build a source map before extracting notes.
   Separate the source into content layers so downstream generation does not mistake product chrome or appendix material for the main argument:
   - core content: the paragraphs carrying the main argument
   - support content: evidence, examples, metrics, or side explanations that materially support the core content
   - noise / annex: related links, product docs, repeated navigation text, operational instructions, or clipped fragments that should not become permanent notes unless the user explicitly wants them

   Record:
   - a one-line thesis for the source
   - a short structure map showing how the main sections connect
   - any boundary judgment that excludes noisy or mixed-in material from note extraction
   - only when useful, a very short argument skeleton such as claim -> evidence -> mechanism -> constraint

3. Extract reusable material.
   Keep only information needed for downstream note generation:
   - key concepts and entities
   - main claims
   - evidence strength
   - a few source-level tensions or caveats that affect confidence or scope
   - contradictions with existing notes when they matter
   - explicit URLs, citations, timestamps, jump links
   - images that materially aid understanding
   - stable named items that may need `wiki/reference-notes/`
   - raw note units that can later become permanent notes

4. Judge wiki fit.
   For each candidate note, decide only:
   - what permanent note may be created or updated
   - whether the candidate repeats, extends, corrects, narrows, or challenges an existing permanent note
   - which existing argument notes are plausibly related
   - whether no existing argument fits and a new argument may be needed
   - whether a reference note may be needed

   Start from argument fit, not only topic fit.
   Prefer updating an existing permanent note when the source adds a clearer wording, stronger evidence, a caveat, an example, a correction, or a source link for the same reusable claim.
   Propose a new permanent note only when the candidate carries a distinct claim, method, distinction, question, or role in an argument chain.
   Do not assign final insertion position, `next` links, or final structure placement here.
   When proposing a possible new argument, use a short parent question by default instead of a long scoped title. Keep qualifiers for `wiki-generation` to decide in the downstream summary and chain.

5. Preserve source reopening aids.
   - Keep useful source links.
   - Keep useful images with Obsidian embeds such as `![[file.ext]]`.
   - Keep short section anchors or textual reopening cues when the source is long, mixed, or easy to misread later.
   - If an image is missing, record that gap clearly.

6. Write the handoff document.
   - Follow `references/output-schema.md`.
   - Keep the file concise and machine-friendly.
   - Do not omit evidence, links, or images that affect generation quality.
   - Record candidate relationships as hypotheses for `wiki-generation`, not final structural edits.
   - Write summaries, claims, and note-unit descriptions as direct statements, not as self-referential setup about what the section is doing.
   - Do not use low-information scaffolding such as “这条笔记回答的问题是：”, “回答：”, “这条链处理……”, or similar template phrasing in the handoff document.
   - When the source is mixed-quality or partially clipped, explicitly mark what was ignored and why.
   - Prefer extraction that helps a later agent reopen the source at the right section instead of rereading the whole file.
   - If you add tensions, keep only 1-3 items that materially affect note generation, placement, or confidence. Do not turn the handoff into a reading companion or brainstorming memo.

## Hard Rules

- Do not write notes into `wiki/`.
- Do not archive the source here.
- Do not silently drop useful links or images.
- Do not silently promote annex material, related-post blocks, navigation text, or product how-to fragments into core claims.
- Do not decide `supports` / `next` links here.
- Do not decide exact argument insertion positions here.
- If no suitable argument target exists, say so explicitly in the analysis file.

## Completion Test

The skill is complete only when:
- `.cache/<source-id>-analysis.md` exists
- the file is enough for `wiki-generation` to work without reopening the source for basic content extraction
- candidate permanent / related argument / possible new argument / reference-note signals are stated clearly
