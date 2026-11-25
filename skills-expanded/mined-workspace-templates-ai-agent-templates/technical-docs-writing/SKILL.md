---
name: technical-docs-writing
description: Writes READMEs and how-to guides a stranger can follow, by running every step itself and cutting anything the reader does not need on first use.
---

# Technical docs writing

Write for one reader, who is new and in a hurry.

## Steps

1. Decide the reader and the goal in one line ("a backend developer who wants the API running locally in ten minutes"). Choose one doc type: tutorial (learn by doing), how-to (solve one task), reference (look things up) or explanation (why). Do not mix them in one page.
2. Read the code, config and existing docs. Collect the real commands, versions, ports and environment variable names. Never invent a flag or path.
3. For a README, use this order: one sentence on what it is and who it is for; a minimal quick start (install, configure, run, expected output); usage with two or three real examples; configuration table; how to test and contribute; license. Put the quick start above the fold.
4. Write steps as numbered imperatives with one action each, the exact command in a code block, and the expected result. Say where to run it. State prerequisites with versions up front.
5. Run every command from a clean clone or container. Fix the doc, or the code, wherever it fails. Paste real output, not imagined output.
6. Edit: short sentences, active voice, same word for the same thing, no "simply" or "just", define a term at first use, link instead of repeating.
7. Add a troubleshooting section for the two or three errors you actually hit.

## Rules

- Do not document unreleased or unverified behavior.
- Keep the diff to docs unless you found a bug; report bugs separately.

## Report

The files written, which steps you verified by running them, and what you could not verify.
