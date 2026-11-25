---
name: refactoring-planner
description: Use to design safe, behavior-preserving refactoring waves from repository evidence.
---

# Refactoring Planner Skill

## Purpose

Plan refactoring without accidental behavior change.

## When to use

Use before broad cleanup, architecture alignment, package restructuring, or modernization.

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
