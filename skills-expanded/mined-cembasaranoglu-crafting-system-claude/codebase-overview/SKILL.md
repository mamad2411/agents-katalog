---
name: codebase-overview
description: Use to answer high-level and low-level questions about repository structure, runtime surfaces, and source paths.
---

# Codebase Overview Skill

## Purpose

Help Claude produce evidence-backed codebase overviews.

## When to use

Use when the user asks how the project works, where something lives, or what path owns a feature.

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
