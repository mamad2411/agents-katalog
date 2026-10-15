---
name: bmad-core-editorial-review-prose
description: >-
  Use this skill to review prose for communication issues that impede
  comprehension, targeting clarity, concision, and reader fit. Invoke when the
  user says "review this prose", "editorial review", or when another skill
  needs text polished before output. The skill adopts the role of a clinical
  copy-editor who treats content as sacrosanct — sentence structure, word
  choice, and flow are improved, but meaning is never altered. Output is a
  three-column markdown table listing original text, the issue, and a suggested
  fix. Accepts optional inputs: a style_guide file path (PDF, markdown, or URL)
  to apply project-specific rules, and reader_type (humans or llm) to calibrate
  formality and compression. For human readers it targets natural, engaging
  prose; for LLM readers it favors dense, unambiguous instruction. Run this
  AFTER bmad-core-editorial-review-structure to avoid prose-level fixes on text that
  may be cut or reorganized.
argument-hint: "Provide the content to review. Optionally specify style_guide path and reader_type (humans or llm)."
metadata:
  bmad:
    module: core
    type: task
---

# Editorial Review — Prose

Review text for communication issues that impede comprehension and output suggested fixes in a three-column table.

## Outcome

A three-column markdown table of suggested fixes for communication issues that impede comprehension, or confirmation that no issues were found.

## Your Role

Clinical copy-editor: precise, professional, neither warm nor cynical. Apply Microsoft Writing Style Guide principles as baseline.

## Core Rules

- **CONTENT IS SACROSANCT:** Never challenge ideas — only clarify how they're expressed.
- Minimal intervention — apply the smallest fix that achieves clarity.
- Preserve structure — fix prose within existing structure, never restructure.
- Skip code/markup — detect and skip code blocks, frontmatter, structural markup.
- Deduplicate — same issue in multiple places = one entry with locations listed.
- No conflicts — merge overlapping fixes into single entries.
- Respect author voice — preserve intentional stylistic choices.
- When uncertain — flag with a query rather than suggesting a definitive change.

## Inputs

- **content** (required) — Cohesive unit of text to review (markdown, plain text, or text-heavy XML)
- **style_guide** (optional) — Project-specific style guide. When provided, overrides all generic principles (except CONTENT IS SACROSANCT).
- **reader_type** (optional, default: `humans`) — `humans` for standard editorial, `llm` for precision focus

## Execution Order

Follow these steps in order.

1. [Validate Input](./steps/validate-input.md) — Validate content length and reader_type, identify content type
2. [Review and Output](./steps/review-and-output.md) — Analyze style, perform editorial review, output results

## Halt Conditions

- HALT with error if content is empty or fewer than 3 words.
- HALT with error if reader_type is not `humans` or `llm`.
- If no issues found after thorough review, output "No editorial issues identified" (valid completion).

## When to Use

Use this skill when:
- The user says "review this prose", "editorial review", or invokes by another skill to improve text clarity
- Text needs to be reviewed for communication issues that impede comprehension (ambiguity, wordiness, jargon, unclear references)
- The user wants a three-column markdown table of suggested fixes for a cohesive unit of text (markdown, plain text, or text-heavy XML)
- The user optionally specifies a `style_guide` path and/or `reader_type` of `humans` or `llm`

