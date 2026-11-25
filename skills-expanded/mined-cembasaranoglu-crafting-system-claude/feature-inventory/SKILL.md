---
name: feature-inventory
description: Use to classify feature status as implemented, partial, docs-only, mock-only, test-only, not found, or unknown.
---

# Feature Inventory Skill

## Purpose

Prevent overclaiming feature readiness.

## When to use

Use when the user asks what features exist, what is missing, or what is production-ready.

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
