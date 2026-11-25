---
name: sage-discipline-systematic-debugging
description: SAGE — root cause before fixes. For tracebacks, failing tests, build errors, and unexpected behavior.
---

# SAGE discipline — Systematic debugging

## Purpose

**SAGE** agents must **investigate before patching**. Guessing creates churn and hides the real defect.

**Core rule:** No fix without a supported root-cause story tied to evidence (logs, stack traces, minimal repro).

## Iron law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## Phase 1 — Understand

1. Read the **full** error message and stack trace (file:line).
2. **Reproduce** reliably; note exact steps and environment.
3. **Diff / history**: what changed recently? deps, config, files.
4. For multi-component flows, narrow **which layer** fails (don’t fix the wrong tier).

## Phase 2 — Hypothesis

- One primary hypothesis; test it with the smallest experiment (log line, assert, isolated run).

## Phase 3 — Fix

- Smallest change that addresses the root cause; add a regression test when applicable.

## Phase 4 — Verify

- Run the same verification you would use for completion (**sage:discipline:verification-before-completion**).

## Cross-links

- **sage:discipline:test-driven-development** — add a failing test that captures the bug when possible.
