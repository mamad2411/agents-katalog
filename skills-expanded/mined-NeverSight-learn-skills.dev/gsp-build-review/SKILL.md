---
name: gsp-build-review
description: "Use when reviewing a built or in-progress game against the locked brief before claiming completion."
---

# Game Build Review

## Goal
Default review stage between implementation and runtime verification. Catch shape drift, weak scope decisions, and fake-complete output before verifier time is spent.

## Outputs

Follow the `gsp-orchestrator` output strategy:
- **inline** (default): present review findings in conversation.
- **minimal** or **full**: write `docs/game-studio/build-review.md`.

## Review focus
- does the current build still match the locked game form
- does the implementation match the approved brief and current task plan
- are the requested core verbs and loops actually present
- is the result fake-complete, placeholder-heavy, or missing obvious quality-critical work
- did the builder introduce unnecessary complexity or unrelated scope
- are the next fixes better handled before runtime verification

## Reporting rules
For each issue, report:
- severity: critical / important / minor
- evidence source
- short repair direction

## Important
This is not the runtime verifier.
Review the implementation against the concept, brief, and plan so the verifier receives a build worth testing.
