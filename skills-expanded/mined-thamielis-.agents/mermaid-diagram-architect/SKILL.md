---
name: mermaid-diagram-architect
description: Build valid, advanced Mermaid diagrams from requirements and repair broken Mermaid syntax quickly. This skill should be used when users ask to create, improve, debug, or standardize Mermaid flowcharts and other Mermaid diagram types.
---

# Mermaid Diagram Architect

## Overview

Generate Mermaid diagrams that are syntactically valid, semantically clear, and easy to maintain. Select the right diagram type, apply layout and style intentionally, and verify parser-safe output before delivering.

## Use Cases

Apply this skill when requests involve:

- Creating a Mermaid diagram from text requirements
- Converting architecture/process notes into Mermaid syntax
- Debugging Mermaid parse/render errors
- Refactoring large or messy Mermaid diagrams
- Standardizing Mermaid code style for documentation repos
- Rendering Mermaid diagrams to SVG/PNG/PDF with CLI

## Workflow

### 1. Classify the Diagram Intent

Determine the primary communication goal first, then pick one diagram type.

- Process flow or decision logic: `flowchart`
- Interactions over time: `sequenceDiagram`
- Domain model with entities/relations: `erDiagram`
- State transitions: `stateDiagram-v2`
- Timeline/roadmap: `timeline` or `gantt`
- Code/package structure: `classDiagram`

Use `references/diagram-selection-matrix.md` for quick mapping from intent to syntax starter.

### 2. Build an Abstract Diagram Plan

Define structure before syntax.

- List nodes/entities/actors/states
- List relationships with direction and labels
- Group clusters or subgraphs
- Set one reading direction (`LR`, `TB`, etc.) when supported
- Keep labels concise and domain-specific

Avoid emitting Mermaid code until the structural plan is coherent.

### 3. Generate Mermaid Syntax

Emit minimal valid syntax first, then enrich.

- Start with a diagram declaration line (for example `flowchart LR`)
- Add nodes first, then edges/relations
- Add labels only where needed for disambiguation
- Prefer stable node IDs and readable labels
- Keep one statement per line for diff readability

Use `references/flowchart-advanced-patterns.md` for advanced flowchart constructs and safe idioms.

### 4. Apply Layout and Styling Deliberately

Configure only what improves readability.

- Use `%%{init: {...}}%%` for diagram-local options
- Use `theme: "base"` when customizing `themeVariables`
- Use renderer/layout options (for example ELK) only when complexity warrants it
- Add classes and styles for semantic emphasis, not decoration

Use `references/mermaid-validity-checklist.md` for parser-safe config patterns.

### 5. Validate Before Delivery

Run a strict validity pass before returning final code.

- Confirm declaration matches syntax used
- Confirm every referenced node/entity is defined or valid inline
- Confirm no known breaker patterns remain
- Confirm labels requiring quoting are quoted
- Confirm directives/frontmatter are syntactically correct JSON/YAML blocks
- Confirm code block fencing matches target environment

Apply the checklist in `references/mermaid-validity-checklist.md`.

Run automated validation when a local file exists:

`python scripts/validate_and_render_mermaid.py --input diagram.mmd --check-only`

### 6. Repair Errors Systematically

When parser errors occur, isolate and fix incrementally.

1. Reduce to a minimal reproducer
2. Re-add sections in small chunks
3. Validate after each chunk
4. Reintroduce styling/config last

Prioritize fixing declaration mismatch, malformed directives, reserved token collisions, and quoting issues first.

### 7. Deliver Multi-Format Output

Return output in the format the user needs.

- Markdown fenced block for docs/wiki use
- Raw `.mmd` content for CLI/render pipelines
- Optional `mmdc` command examples for image export

If CLI rendering is requested, reference `scripts/validate_and_render_mermaid.py` or the commands in `assets/templates/cli-rendering-examples.md`.

## Automation

Use the wrapper script for deterministic validation and rendering:

- Validate only: `python scripts/validate_and_render_mermaid.py --input diagram.mmd --check-only`
- Validate and render: `python scripts/validate_and_render_mermaid.py --input diagram.mmd --output diagram.svg`
- Validate and render with config: `python scripts/validate_and_render_mermaid.py --input diagram.mmd --output diagram.png --config mermaid-config.json --scale 2`

If `mmdc` is unavailable, install Mermaid CLI or provide `--mmdc` with an explicit executable path.

## Diagram Validity Rules

Enforce these baseline rules for all Mermaid outputs.

- Declare exactly one diagram type at top of each block
- Keep syntax consistent with that declaration
- Use comments as `%% ...` and avoid directive-like braces in comments
- Quote labels that contain special characters or reserved words
- Avoid ambiguous tokens and accidental operator collisions
- Keep IDs simple (`A1`, `svc_api`, `dbMain`) and stable
- Prefer incremental composition for complex diagrams

## Flowchart-Specific Guardrails

Apply these every time `flowchart` or `graph` is used.

- Avoid lowercase `end` as plain node text; quote or capitalize it
- Avoid unintended circle/cross edges from `---o` or `---x` patterns
- Set explicit direction (`TB`, `LR`, `RL`, `BT`) early
- Use subgraphs only when they improve mental grouping
- Use advanced shapes only when semantic value is clear

## Resource Map

- `scripts/validate_and_render_mermaid.py`: Automated validation/render wrapper around `mmdc`
- `references/diagram-selection-matrix.md`: Intent-to-diagram selection guide with starters
- `references/mermaid-validity-checklist.md`: Parser-safe validation and debugging checklist
- `references/flowchart-advanced-patterns.md`: Advanced flowchart patterns and safe usage rules
- `assets/templates/diagram-starters.md`: Reusable starter snippets for common diagram goals
- `assets/templates/cli-rendering-examples.md`: `mmdc` rendering commands and config patterns