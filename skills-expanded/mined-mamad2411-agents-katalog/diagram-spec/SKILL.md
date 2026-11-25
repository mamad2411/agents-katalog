---
name: diagram-spec
description: Produce Mermaid diagrams for ideas, architecture sketches, and flows — lightweight spec without full wiki generation. Use for quick diagrams; use architecture-atlas for full codebase wikis.
license: MIT
metadata:
  version: "1.0"
---

# Diagram Spec

Quick **Mermaid** diagrams from user descriptions or brief code reads.

## When to Use

- User wants a flowchart, sequence, class, or mindmap in Mermaid
- Brainstorming architecture before implementation
- Embed diagram in PR or doc (not full wiki)

## Tools

- **read_file** — Optional grounding in existing code
- Output Mermaid fenced blocks in chat or **write_file**

## Diagram types

| Type | Use |
|------|-----|
| flowchart TD | Processes, decisions |
| sequenceDiagram | API/interaction order |
| classDiagram | Type relationships |
| erDiagram | Data models |

## Rules

- Keep ≤30 nodes for readability
- Label edges with verb phrases
- Mark `[UNVERIFIED]` nodes not from code

## Provenance

Inspired by Hermes concept-diagrams; minimal Akasha variant.

## Installation

```
Install the diagram-spec skill from https://github.com/azerothl/Akasha_skills/tree/main/skills/diagram-spec
```
