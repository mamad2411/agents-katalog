---
name: cli-output-format-dispatch-with-template
description: CLI accepts --format=json|jsonl|text and an optional --format-str with printf-style placeholders (%p path, %l label, %s score, %i mime, %g group, %b overwrite_reason).
category: cli
version: 1.0.0
version_origin: extracted
confidence: high
tags: [magika, cli]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Cli Output Format Dispatch With Template

**Trigger:** Building a CLI that must output the same data in multiple formats (machine, human, custom column selection) without spawning child tools.

## Steps

- Define a Format enum: JSON, JSONL, TEXT, CUSTOM.
- Parse the custom template string and recognize a fixed set of placeholders; reject unknown ones at parse time.
- Substitute placeholders per result; default to TEXT (human-readable, colored if TTY).
- For TEXT, align columns and use ANSI colors gated by isatty + --no-colors flag.
- For JSON/JSONL/CUSTOM, never emit progress/warnings to stdout — keep stdout machine-parseable.
- Document the placeholder set with examples in --help output.

## Counter / Caveats

- Keep the template grammar simple — no conditionals, no loops, just substitution.
- Aligning columns with Unicode (CJK, emoji) breaks monospace assumptions; document the limitation.
- Changing the default format between releases breaks user scripts; treat the default as a stable API.
- Escape sequences (%, \t, \n) inside templates are confusing; show them in --help with examples.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/cli/src/main.rs:102-230`
- `python/src/magika/cli/magika_client.py:70-85`
