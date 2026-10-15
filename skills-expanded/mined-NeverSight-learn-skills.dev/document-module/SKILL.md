---
name: document-module
description: Write comprehensive module-level AGENTS.md documentation for a module or complex flow.
user-invocable: true
argument-hint: '[module path]'
---

# Module Documentation Writing

Produce a module-level `AGENTS.md` that gives future engineers enough context to work without re-reading the whole source tree.

## Required sections

- title and ownership
- architecture overview
- high-level rules
- key files table
- invariants to protect

## Include when applicable

- entry points
- persisted state / lifecycle
- error management
- common change patterns
- debugging checklist
- test guidance

## CLAUDE reference

If the module directory does not already have `CLAUDE.md`, add:

```markdown
@AGENTS.md
```
