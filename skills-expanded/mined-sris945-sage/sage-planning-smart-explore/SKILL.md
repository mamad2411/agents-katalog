---
name: sage-planning-smart-explore
description: SAGE — explore codebases with structure-first search; minimize full-file reads and token use.
---

# SAGE planning — Smart exploration

## Purpose

In **SAGE**, **map before you read**: find symbols, files, and boundaries before loading large files. This reduces tokens and avoids missing the right module.

## Preferred order

1. **Scope** — Identify language roots (`src/`, `lib/`) from project layout.
2. **Search** — Use targeted search (ripgrep, glob) for symbols, class names, error strings.
3. **Skeleton** — For supported languages, use **structural** understanding (e.g. tree-sitter / semantic outline) when available in the toolchain.
4. **Deep read** — Open only the files and regions that the map says matter.

## What to avoid

- Reading entire large files when a search + partial read suffices.
- Repeated full-directory reads — cache what you learned in **ORCHESTRATOR NOTES** or task context.

## SAGE tools

- **Patch / filesystem tools** follow **WORKSPACE POLICY** — stay inside allowed roots.
- Prefer **grep → read range** over “read whole repo”.

## When to read fully

- Small config files, single-purpose modules, or after you’ve narrowed to one file.

## Cross-links

- **sage:planning:make-plan** — exploration findings feed Phase 0 of the plan.
