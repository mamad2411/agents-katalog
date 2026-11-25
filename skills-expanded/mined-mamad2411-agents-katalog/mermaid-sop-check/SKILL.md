---
name: mermaid-sop-check
description: Use when Codex creates or edits Mermaid diagrams, validates standalone .mmd files, validates Mermaid code blocks embedded in Markdown, or debugs Mermaid parse/render errors before delivery.
---

# Mermaid SOP

## Installation and Environment Check

Install Mermaid CLI globally first:

```bash
npm install -g @mermaid-js/mermaid-cli
```

Confirm the command is available:

```bash
mmdc -V
```

## Workflow

1. Write the Mermaid diagram.
2. Run a self-check against the common syntax pitfalls.
3. Run an `mmdc` render check.
4. If rendering fails, fix the syntax and rerun the check until the exit code is `0`.

## Common Syntax Pitfalls

- Missing or misspelled declaration lines, such as `flowchart TD`, `sequenceDiagram`, or `classDiagram`.
- Mixed diagram types and syntax, such as using sequence diagram syntax inside a `flowchart`.
- Bare `end` text in a `flowchart`, which can cause parse errors. Rename it or quote it.
- Node text that contains special characters without quotes.
- Incorrect `%%` comment syntax or placement that causes parse errors.

## mmdc Check Commands

Check a standalone `.mmd` file:

```bash
mmdc -i <file.mmd> -o /tmp/<name>.svg -q
```

Check Mermaid code blocks inside Markdown (```mermaid ... ```):

```bash
mmdc -i <doc.md> -o /tmp/<name>.check.md -a /tmp/<name>-artefacts -q
```

## Failure Handling Order

1. Return to the common syntax pitfalls and check each item.
2. Fix one issue with the smallest practical change, then rerun `mmdc` immediately.
3. Continue only after the command succeeds with exit code `0`.

## Pre-Delivery Checks

- Run `mmdc` at least once for every new or modified Mermaid diagram.
- Do not skip checks for Mermaid diagrams embedded in Markdown.
- Do not treat visual inspection as a substitute for actual `mmdc` rendering.
