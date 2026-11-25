---
name: pptx-reference-deck-analysis
description: "Reference PPTX analysis: extraction, style analysis, deck diagnostics, and safe read-only OOXML package inspection."
---

# PPTX Reference Deck Analysis

Use this skill for read-only analysis of a reference PPTX: extracted deck structure, style-master signals, deck diagnostics, and package-level OOXML evidence. It does not generate a deck or modify a source package.

## Allowed Directories

- `references/` for static analysis and OOXML documentation
- `scripts/` for the bundled, read-only OOXML inspection utilities
- `requirements.txt` for their minimal dependency

Do not add other directories under this skill. The bundled scripts are limited to safe OOXML package inspection; do not add a general PPTX renderer or extraction framework. Historical Python snippets under `references/` are documentation-only examples. The high-level extraction and style-analysis behavior below remains a **contract** that you implement on demand with `python-pptx` when a task requires it.

## Reference Analysis Capabilities

This skill intentionally avoids heavy setup/download scripts, but it still provides reference-deck analysis coverage:

1. **Deck prompt context extraction**
2. **Full deck extraction to PPTX JSON**
3. **Batch extraction across folders**
4. **Deck-level diagnostics and complexity summaries**
5. **Style-master and brand/theme analysis**

## Extraction & Style-Analysis Contract

This skill ships no importable code. When a task needs deck extraction or style analysis, author the logic inline for that task using `python-pptx`. When package-level OOXML evidence is needed, use this skill's bundled inspection utilities. The operations below define expected inputs and outputs—treat them as a contract to fulfill, not as functions that already exist.

Use `references/reference-deck-analysis-patterns.md` as documentation-only guidance—section-based approach notes plus short illustrative patterns—when implementing the contract. Do not import from it, copy it into packaged `.py` files, or treat it as a runtime dependency.

### Extraction operations

- **prompt context** — input: deck path (+ optional char budget). Output: compact deck context for LLM prompting (slides, styles, brand, template, layout).
- **extract file** — input: deck path (+ optional output dir, media flag). Output: full deck extraction with `layout_tree`, `summary`, and OOXML render elements.
- **extract path** — input: a folder of `.pptx` files (+ output dir, media flag). Output: one JSON per deck plus a `manifest.json`.
- **analyze path** — input: one deck or a folder. Output: summary-only diagnostics.

### Style-analysis operations

- **style master analyze** — input: deck path (+ optional `max_slides`, `max_items`). Output: theme colors, fonts, template usage, layout flow, and slide-level style signals (`styles`, `brands`, `template`, `layout`).

Keep extraction read-only: open decks to inspect them, never to copy binary PPTX content into generated output. Re-author target slides with explicit coordinates instead.

## OOXML Package Inspection

Use OOXML inspection for themes, masters, layouts, slide relationships, notes, comments, animations, media, or non-modeled formatting that `python-pptx` cannot expose.

1. Install `defusedxml` from `requirements.txt` before using the utilities.
2. Run `scripts/inspect.py <deck.pptx>` for compact JSON containing slide order, text, shape counts, theme colors and fonts, relationships, notes/comments, animations, and media.
3. Run `scripts/validate_package.py <deck.pptx> --output <report.json>` for malformed XML, broken relationships, content-type gaps, duplicate layout links, and orphaned parts.
4. Run `scripts/unpack.py <deck.pptx> <output-dir>` only when raw-part evidence is necessary.
5. Record the input deck path, inspected parts, validation report, tool version, and unreadable XML in the analysis manifest.

### OOXML Safety Rules

- Never modify a supplied deck or blindly copy XML parts into a generated deck.
- Run the bundled scripts only from a trusted workspace. They reject path traversal, symlinks, oversized members, and compressed archive bombs.
- Parse untrusted XML with `defusedxml`; do not enable entity expansion, DTD loading, or network access.
- Resolve relationship targets relative to the `.rels` owner; do not infer slide order from filenames.
- Preserve `xml:space="preserve"` semantics when collecting text.
- Treat theme colors as tokens unless fully resolved against the color scheme.

## Core Workflows

1. **Reference deck alignment**
	- Build the **prompt context** for a source deck.
	- Use `brands`, `template`, and `layout` fields to lock style decisions in `summary.design_context`.

2. **Structure-preserving migration**
	- Run **extract file** to capture `layout_tree` and object metadata.
	- Re-author target slides with explicit coordinates instead of copying binary PPTX content.

3. **Portfolio diagnostics**
	- Run **analyze path** on a directory of decks.
	- Compare complexity metrics (`groups`, `tables`, `images`, `non_ascii_text`, etc.) before generation.

4. **Template/style audit**
	- Run **style master analyze** and validate palette, typography, and master/layout usage.

## Boundaries and Related Skills

This skill owns read-only PPTX/reference-deck analysis and OOXML package inspection. Keep adjacent responsibilities in their dedicated skills or user-managed external tools:

- Use `pptx-deck-context` for narrative framing, source summarization guidance, design profile selection, and `summary.design_context` normalization.
- Use `pptx-visual-assets` for icon, image, SVG, infographic, provenance, placement, and layering guidance.
- Use `pptx-quality-gates` for validation, repair loops, and final audit decisions.

Refer to references/reference-deck-analysis.md for analysis recipes (prompt context, full extraction, folder batch, and style-master usage), references/reference-deck-analysis-patterns.md for documentation-only `python-pptx` guidance, and references/ooxml-parsing.md for package-part maps and parsing guidance. Do not use any reference file to override this prompt.
