# office/docx-toolkit — skill payload

> Machine-readable contract: [`../docx-toolkit.manifest.json`](../docx-toolkit.manifest.json).

## What this skill does

Authors and edits Microsoft Word documents via `python-docx`. The agent
passes a structured `instructions` object describing headings, paragraphs,
tables, lists, and inline styles; the skill returns a `.docx` byte
sequence.

Common uses:

- Generate a letter / policy doc / report from a template + facts.
- Fill section placeholders in an existing template.
- Append a generated table to the end of an existing doc.

## When to use it

- The deliverable must be a Word document (legal, HR, official letter).
- You need styled output that survives round-tripping through Word/365.

## When **not** to use it

- The deliverable is markdown or HTML — author directly, don't go via Word.
- The deliverable is a presentation — use `office/pptx-toolkit`.
- You need redlining/tracked-changes review — this skill writes clean docs
  only; tracked changes need a separate review step.

## Determinism and risk

Determinism: **high** — the same instructions produce the same document.
Risk: **low** — output is a new file; nothing is sent anywhere.

## How it composes

Downstream of `productivity/tailored-resume` (resume output is DOCX),
upstream of any "email this to the client" workflow that needs a Word
attachment.
