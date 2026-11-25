---
name: sage-workflow-tdd
description: SAGE — structured TDD workflow for features and fixes; align tests with user-visible behavior.
---

# SAGE workflow — TDD workflow

## Purpose

Use in **SAGE** coding tasks to keep work **test-backed** end-to-end: unit coverage for logic, integration for boundaries, targeted E2E only where it earns its cost.

## Principles

1. **Tests before implementation** for new behavior (see **sage:discipline:test-driven-development**).
2. **Coverage** — aim high on critical paths; don’t chase numbers on trivial getters.
3. **Layers**
   - Unit: pure logic, helpers, small modules.
   - Integration: DB, HTTP, subprocess boundaries (with fakes or test doubles where appropriate).
   - E2E: few journeys that prove the product path works.

## Steps

1. Name the user-visible outcome (one sentence).
2. List failure modes and edge cases; each gets a test name before code.
3. Implement until green; refactor; re-run the suite you care about.

## SAGE-specific

- Respect **TOOL PERMISSIONS** and **WORKSPACE POLICY** in the universal prefix.
- Prefer project’s existing test runner (`pytest`, `npm test`, etc.) — discover from `pyproject.toml`, `package.json`, or `Makefile`.
