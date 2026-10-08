---
name: drastic-paladin
description: Identify dead code, fallback residue, mocks, TODOs, and cleanup candidates with evidence-backed prioritization.
---

# Drastic Paladin

## Purpose

Use this skill for deletion/governance passes over dead code, residue, and stale surfaces.

## When To Use

Use `drastic-paladin` when:

- the user invokes `paladin`,
- the task is to find dead code, fallback branches, TODO/mock residue, or stale modules,
- cleanup needs evidence before deletion.

## Responsibilities

1. Scan usage, entrypoints, tests, and change history for cleanup candidates.
2. Classify findings as `confirmed-dead`, `likely-dead`, `legacy-bridge`, `fallback-mask`, `hygiene-residue`, or `needs-verify`.
3. Prioritize immediate debt-prevention removals in pre-user surfaces.
4. Produce concrete action recommendations with confidence and validation method.
5. Do not delete by default in this mode unless explicitly asked.
6. Respect component-library inventory guardrails for managed UI component surfaces.

## Output Contract

- `Summary`
- `Dead/legacy candidates`
- `Fallback/todo/mock candidates`
- `Evidence`
- `Recommended actions`
- `Open questions/risks`

## Guardrails

- Findings must be path-specific and reproducible.
- Do not recommend component-library deletion from static usage evidence alone.
- Keep recommendations rollback-safe and sequence-aware.
- Skill-local flow must not override shared routing, planning, verification, or commit rules.
