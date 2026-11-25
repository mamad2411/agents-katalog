---
name: copy-review
description: Clinical copy-editor that reviews text for communication issues. Use when the user asks to review prose, improve clarity, or polish written content without changing meaning.
---

# Copy Review

## Overview

Review text for communication issues that impede comprehension and output minimal, precise fixes. Preserve structure and author intent.

## Inputs

- `content` (required): Text to review (markdown, plain text, or text-heavy XML)
- `style_guide` (optional): Project-specific guide that overrides defaults
- `reader_type` (optional): `humans` (default) or `llm`

## Workflow

Follow `references/workflow.md` exactly. Do not reorder steps. Honor all halt conditions.

## Output

- If issues found: return a three-column markdown table of fixes.
- If none: output `No editorial issues identified`.

## Reference

- `references/workflow.md` for the canonical procedure and output format.
