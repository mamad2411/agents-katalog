---
name: style-fingerprint-gate
description: Use before delivering formal academic, reviewer-facing, stakeholder-facing, or submission-facing prose to scan and reduce overused binary negative-contrast constructions such as "rather than", "not...but", "不是...而是", and "而不是"; runs after self-review and before final delivery.
---

# Style Fingerprint Gate

Use this skill for proposals, literature reviews, methodology sections, manuscripts, reports, theses/dissertations, supervisor/PI-facing drafts, reviewer-facing drafts, bilingual drafts, and formal academic prose.

## Purpose

Catch repeated binary negative-contrast constructions before delivery. This is a deterministic style-density check, not an AI detector and not a detector-evasion workflow.

## Required Position

Run after:

- `academic-self-review-loop`
- academic register / authorial voice drafting

Run before:

- final artifact generation
- pre-delivery lock
- `scripts/formal_delivery_guard.py`
- final delivery summary

## Workflow

1. Run the scanner on the source Markdown or extracted text:

   ```bash
   python3 scripts/style_fingerprint_scan.py <draft> --strict
   ```

   The scanner checks three failure modes:

   - density per 1000 estimated words;
   - total number of negative-contrast hits;
   - repeated use of the same pattern category, even in a long document.

2. If density is above threshold:

   - locate each flagged construction;
   - keep only genuine scope distinctions;
   - rewrite mechanical instances into direct positive statements, conditional clauses, or plain definitions;
   - avoid changing argument structure, evidence meaning, citations, or uncertainty level.

3. Re-run the scanner.

4. If any downstream skill edits the prose after the scan, re-run the scanner on the final source text before Word generation or delivery.

5. Record before/after density in the writing checkpoint or delivery checkpoint.

## Pattern Inventory

The scanner looks for repeated surface patterns that caused the Production failure and nearby variants:

English:

- `rather than`: common mechanical contrast marker in the failed draft;
- `not just ... but`: repeated emphasis-stacking pattern;
- `not only ... but`: repeated emphasis-stacking pattern;
- `it's not ... it's`: conversational binary reframing;
- `isn't about ... it's about`: conversational binary reframing;
- `not ... but rather`: formal binary reframing;
- `not ... but`: generic binary reframing, counted only when it does not overlap a more specific match;
- `as opposed to`: contrast marker often used where a direct scope statement would be cleaner;
- `instead of ... it`: indirect contrast pattern that often creates a foil before the main claim.

Chinese:

- `并不是...而是`
- `并非...而是`
- `不是...而是`
- `不是...而不是`
- `而不是`
- `而非`
- `不仅...而是`
- `与其说...不如说`
- `不在于...而在于`

The scanner suppresses overlapping matches on the same line so one phrase is not counted twice when a specific pattern already covers it.

## Threshold Rationale

Default hard thresholds:

- density: more than 3 hits per 1000 estimated words;
- total hits: more than 12 hits;
- single category repetition: more than 6 hits in one category.

Default review threshold:

- density above 1.5 hits per 1000 estimated words creates a `REVIEW` status;
- repeated use of one category above the review limit also creates a `REVIEW` status.

Rationale:

- Repeated binary negative-contrast templates can make research prose feel mechanical even when the evidence is sound.
- Some long documents can hide a repeated template under a tolerable density score, so category caps are also required.
- One or two contrastive phrases can be academically legitimate, especially for scope and limitation.
- Above three hits per 1000 estimated words, the pattern becomes visible enough to require human review before formal delivery.

This threshold is a project style gate, not an institutional, journal, funder, or client requirement.

## Scanner Exclusions

The scanner skips:

- fenced code blocks;
- top YAML frontmatter;
- blockquote lines;
- final `References`, `Bibliography`, `Reference list`, `Works cited`, or `参考文献` sections, whether written as Markdown `#` headings, plain standalone headings, or setext-style headings.

It may still flag inline quotations or unusual formatting. Treat those as human-review items, not automatic rewrite instructions.

## Rewrite Preferences

Prefer:

- direct positive statement: say what the research does or shows;
- conditional boundary: state where a claim applies;
- plain definition: define the concept without first rejecting a foil.

Avoid repeated:

- `rather than`
- `not ... but`
- `not only ... but`
- `不是...而是`
- `而不是`
- `并不是...而是`

## Bilingual Rule

For bilingual output, fix the English source first. Then regenerate the Chinese from the cleaned English so the Chinese does not inherit `rather than -> 而不是` translation patterns.

## Override Path

If a legitimate contrast-heavy passage is blocked, do not silently bypass the gate. Record the reason in the writing or delivery checkpoint and, for formal delivery, use `scripts/formal_delivery_guard.py --acknowledge-override --override-reason "<reason>"` only after the user explicitly accepts the remaining style risk.

## Boundaries

- Do not delete every negation.
- Do not remove legitimate academic scope distinctions.
- Do not change source claims, citations, methods, compliance wording, or verified requirements.
- Do not promise that the text will pass an AI detector.
- If the scan finds prompt residue, placeholders, fake references, or misleading AI-use disclosure, route to `academic-integrity-preflight`.
