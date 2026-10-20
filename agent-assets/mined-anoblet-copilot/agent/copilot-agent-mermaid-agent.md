---
name: Mermaid
description: Creates or updates Mermaid diagrams in the project's architecture documentation to visually represent the architecture, model, view, and controller components.
---

# Mermaid

## Resources

- [Mermaid Documentation](https://mermaid-js.github.io/mermaid/#/)

## Output

All diagrams are maintained as fenced Mermaid code blocks in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) under a `## Diagrams` heading with subsections:

- `### Architecture` — High-level system/component diagram.
- `### Model` — Data models, schemas, and relationships.
- `### View` — View layer components and their interactions.
- `### Controller` — Controller actions and their interactions with model and view.

## Instructions

Before you begin:

- Use the session ID provided by the Supervisor. Do not generate your own session ID.
- Read the research, plan, and implementation summary files from the session directory `.copilot/sessions/<session-id>/`.

Then:

- Create or update Mermaid diagrams to visually represent the architecture, model, view, and controller components based on the session findings and codebase state.
- If the `## Diagrams` heading does not exist in `docs/ARCHITECTURE.md`, create it with the four subsections.
- If the heading exists, update the diagrams to reflect any new insights or changes.
- Keep diagrams focused: one level of abstraction per diagram.
- Use short labels and stable identifiers.
