---
name: diagram-policy
description: Use when the task involves architecture, infra, data flow, integration, orchestration, migration, or debugging chains and needs the right diagram type.
---

# Diagram Policy

Pick the lightest diagram that answers the question:
- ASCII architecture: components and boundaries
- sequence: interaction order
- data-flow: pipeline and transformations
- ERD: schema shape
- state machine: lifecycle and transitions
- component/screen map: dashboards, workflow surfaces, navigation

A diagram should expose ownership, order, and likely failure points.

Selection heuristic:
- "What exists and how is it split?" -> ASCII architecture
- "Who calls whom and when?" -> sequence
- "Where does data move?" -> data-flow
- "How is data shaped?" -> ERD
- "How does it evolve?" -> state machine
- "What does the surface look like?" -> component/screen map

Reference:
- `~/.ai-agent-hub/knowledge/rules/operator-pack-v3/DIAGRAM_TAXONOMY.md`
