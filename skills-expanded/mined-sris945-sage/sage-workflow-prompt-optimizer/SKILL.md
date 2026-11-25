---
name: sage-workflow-prompt-optimizer
description: SAGE — advisory only. Improve how the user phrases goals for the SAGE pipeline; do not execute their task inside this mode.
---

# SAGE workflow — Prompt optimization (advisory)

## Purpose

When the user asks to **improve a prompt** or **rewrite instructions** for **SAGE** (`sage run`, agents, tasks), help them produce a **clear, scoped, verifiable** goal. This skill is **advisory**: do not implement the project here unless the user switches to a normal execution request.

## When to use

- “Optimize this prompt”, “make this clearer for SAGE”, “how should I ask for X?”
- Draft goals that lack acceptance criteria or scope.

## When not to use

- User wants immediate implementation — use normal SAGE execution, not prompt-only mode.
- Pure code/perf optimization requests — those are engineering tasks, not prompt editing.

## Output shape

1. **Intent** — what success looks like in one paragraph.
2. **Scope** — in/out (files, tech, non-goals).
3. **Acceptance** — checks that prove done (commands, behaviors).
4. **Ready-to-run prompt** — a single block the user can pass to `sage run "..."`.

## Tone

- Plain, imperative language; no filler.
- Reference **SAGE** concepts: agents, workspace, verification, tool permissions when relevant.
