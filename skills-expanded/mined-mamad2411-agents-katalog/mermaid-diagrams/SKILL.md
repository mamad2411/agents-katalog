---
name: mermaid-diagrams
description: Use Mermaid diagrams instead of ASCII art.
---

# Mermaid diagrams

Write all documentation diagrams as Mermaid; do not use ASCII art.

**Why:** ASCII art breaks on reflow, is not diffable line-by-line, and does not render as a graphic in GitHub — so diagrams rot silently and reviewers cannot tell what changed.

## When to use

- Architecture and flow diagrams in `docs/wiki/`
- Any diagram that shows relationships, sequences, or data flow

## Patterns

- Use `flowchart TD` or `flowchart LR` for flow/architecture diagrams
- Use `sequenceDiagram` for request/response flows
- Use `classDiagram` for type relationships

## Examples

````text
// BAD — ASCII art; hard to maintain, not diffable
Client --> [Auth] --> [API] --> [DB]
     ^                  |
     +------------------+

// GOOD — Mermaid; readable, maintainable, renders in GitHub
```mermaid
flowchart LR
    Client --> Auth
    Auth --> API
    API --> DB
    API --> Client
```
````
