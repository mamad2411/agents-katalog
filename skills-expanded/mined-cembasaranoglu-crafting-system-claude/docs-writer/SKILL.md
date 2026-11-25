---
name: docs-writer
description: Use to write README, OSS docs, docs maps, and AI context docs from repository truth.
---

# Documentation Writer Skill

## Purpose

Keep docs accurate, searchable, and safe for OSS/internal handoff.

## When to use

Use when creating or updating README, docs, OSS readiness materials, or AI context files.

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
