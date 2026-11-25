---
name: project-glossary
description: Use to explain project terms, domain vocabulary, technical jargon, and non-technical meanings from repository evidence.
---

# Project Glossary Skill

## Purpose

Maintain consistent technical and non-technical vocabulary for the project.

## When to use

Use when the user asks what a term means, how domain concepts relate, or how to explain the codebase to non-technical readers.

## Inputs to inspect first

- `CLAUDE.md`
- `docs/AI_CONTEXT.md`
- `docs/PROJECT_GLOSSARY.md`
- `docs/FEATURE_INVENTORY.md`
- relevant source paths

## Rules

- Inspect source evidence before answering.
- Distinguish facts, assumptions, recommendations, unknowns, blockers, and validation status.
- Do not modify source code unless the user explicitly asks.
- Do not claim tests/builds/deployments ran unless they actually ran.

## Output

Produce:
1. direct answer
2. evidence paths
3. confidence
4. unknowns
5. next action
