---
name: mols-agent-asset-studio
description: >-
  Manage agent assets across creation, improvement, validation, naming,
  optimization, and routing. Use when requests involve agent skills, rules,
  workflows, prompts, or bundled resources, including structuring or
  consolidating them. Does not apply to general application code, merely
  invoking an existing skill, or human-facing documentation.
compatibility: "Requires Agent Skill `mols-markdown-scripts`, Python >=3.13, rumdl, pyromark, pyyaml"
---

## Goal

Manage agent assets.

## Routing

1. Read `workflows/INDEX.csv` once.
2. Identify the requested outcome, operation, object, and constraints.
3. Compare the request with each workflow `description`.
4. Select the minimum workflow set covering the request.
5. Resolve material ambiguity with one targeted question.
6. Resolve each selected `name` as `workflows/<name>.md`.
7. Load referenced resources only when a selected workflow requires them.
8. Run each selected workflow's validation before completion.

Route by semantic intent, not keyword overlap. Do not scan `workflows/` to discover routes.

## Ambiguity

- Select one route when it fully covers the request.
- Select multiple routes only when the request explicitly spans them.
- Ask one targeted question when remaining routes imply materially different actions.
- If no route matches, state that the skill does not cover the request.
