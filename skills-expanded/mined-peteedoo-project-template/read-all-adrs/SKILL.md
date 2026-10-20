---
name: read-all-adrs
description: Read every ADR markdown file in docs/adr before making or reviewing decision-sensitive changes. Use when architecture, conventions, or tradeoffs are involved.
disable-model-invocation: true
---

# Read All ADRs

Read **every** `.md` file in `docs/adr/`, start to finish.

## When to use

- The task changes architecture, workflow, or team conventions.
- You need full context on why prior decisions were made.
- You are unsure whether a proposed change conflicts with accepted ADRs.

## Procedure

1. Enumerate all ADR files in `docs/adr/`.
2. Read each file fully (not just titles/snippets).
3. Capture key constraints and consequences from each ADR.
4. If a conflict appears, call it out explicitly before implementation.

## Output

Produce a concise decision-context summary:

- ADRs read
- Constraints to preserve
- Proposed change fit/conflicts
