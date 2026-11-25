---
name: speckit.debug
description: Systematic Debugger - Reproduce, isolate, prove root causes, and produce a scoped fix plan.
---

## Mission
Find the smallest proven root cause without changing production code during investigation.

## Inputs and Outputs
- Read the issue report, logs, source, configuration, recent changes, and constitution.
- Write `.agents/debug/[issue-slug].md` with timeline, reproduction, hypotheses, evidence, root cause, impact, and fix plan.

## Protocol
1. Record expected versus actual behavior, environment, first-known-good/bad revision, exact reproduction, frequency, and severity.
2. Reproduce with the smallest deterministic command or test; capture bounded logs and inputs without secrets.
3. Trace callers and data/control flow. Form ranked hypotheses, then run one falsifiable check per hypothesis.
4. Identify the exact failing condition and explain why it produces the symptom. Separate trigger, root cause, contributing factors, and non-causes.
5. Define a minimal fix, regression test, blast radius, rollback, and follow-up debt. Hand implementation to `speckit.implement`.

## Completion Gate
Root cause is tied to file/line or configuration evidence, reproduction is recorded, and the fix plan has verification and rollback criteria.

## Guard Rails
Read-only during diagnosis. Do not guess, patch symptoms across callers, expose secrets, or close an issue without reproducible evidence.