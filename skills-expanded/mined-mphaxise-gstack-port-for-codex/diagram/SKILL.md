---
name: diagram
description: Turn an architecture, workflow, or system description into a source-backed diagram artifact for Codex users.
---

# Diagram

Use this skill when the user asks to make, draw, visualize, or refine a diagram.

This port is adapted from `garrytan/gstack` at commit `11de390be1be6849eb9a15f91ff4922dd16c589a`.

## Workflow

1. Clarify the diagram target only if the request is ambiguous:
   - audience
   - format
   - scope
   - level of detail
2. Choose the simplest useful representation:
   - Mermaid for architecture, flowcharts, sequences, and dependency maps
   - Markdown tables for matrices and responsibility maps
   - generated or editable image artifacts only when the user asks for a visual deliverable
3. Build from real repo or source evidence when the diagram describes an existing system.
4. Keep the diagram source editable and include it in the answer or in a requested artifact file.
5. Verify syntax when a local renderer or parser is available.

## Codex Adaptation

- Prefer inline Mermaid for quick diagrams because Codex can render it directly in chat.
- Use local files only when the user asks for a saved artifact or the diagram is too large for chat.
- Do not rely on upstream Claude paths such as `~/.claude/skills/gstack` or bundled Excalidraw helpers.
- If image generation or conversion tools are unavailable, return the editable source and state the missing renderer plainly.

## Guardrails

- Do not invent system structure when repo evidence is available.
- Do not produce a decorative diagram when the user needs an operational one.
- Do not hide uncertainty; mark inferred edges or speculative components.
- Keep labels short enough to render cleanly.
