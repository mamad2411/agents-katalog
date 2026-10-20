---
name: vitest-engineering
description: Write and configure Vitest tests. Use when working on a Vite/Vitest project.
metadata:
  tags: vitest, engineering
---

# Vitest Engineering

## Use this skill when
- Configuring Vitest and environments
- Using vi mocks, fake timers, and test isolation
- Fast watch-based TDD

## Do not use this skill when
- Non-Vite/JS projects
- Testing design (use unit-testing)

## Instructions
1. Match project structure for ms*paths and environment (node/jsdom/happy-dom).
2. Use vi and globals deliberately; keep isolation with beforeEach.
3. Prefer fakeTimers for time logic; control with advanceTimers.
4. Use setupFiles for global stubs; clear all mocks between tests.
5. Define workspace/project configs for monorepos.
6. Set coverage thresholds where they add value.

## Checklist
- Mocks cleared between tests
- Environments are correct per test
- Fast enough for TDD

## Output Format
- Config | environment map | isolation policy

## Common Mistakes
- Everything in jsdom bloating speed
- Mock hoisting surprises (vi.mock)|Misconfigured workspace
