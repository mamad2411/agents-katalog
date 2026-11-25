---
name: diagram-as-code
description: Produces Mermaid diagrams of flows, sequences and data models read from the actual code, ready to commit next to your docs.
---

# Diagram as code

Draw what the code does. Every box must trace to a file, table or service.

## Steps

1. Clarify the question the diagram answers (how a request flows, how services talk, what states an order has, how tables relate). One question per diagram.
2. Choose the type: `sequenceDiagram` for interactions over time, `flowchart` for decisions and pipelines, `stateDiagram-v2` for lifecycles, `erDiagram` for data models, `classDiagram` only for real type hierarchies.
3. Trace the code: start at the entry point (route, handler, job, CLI) and follow calls, queries and outgoing requests. For data models read migrations or ORM models for tables, keys and relations.
4. Write the Mermaid. Use real names from the code for nodes. Keep it to roughly 12 nodes; split into two diagrams when larger. Label edges with the verb or payload.
5. Check syntax: keep labels with brackets or colons in quotes, avoid reserved word `end` as a node id, and render with `npx @mermaid-js/mermaid-cli` if available.
6. Place the diagram in a Markdown file in a `mermaid` fenced block, with two sentences of explanation above it.

## Rules

- No invented components or "future" boxes.
- Do not draw every function; show boundaries that matter.
- Note what you left out below the diagram.

## Report

File path, what question each diagram answers, and the source files you traced.
