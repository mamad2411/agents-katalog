---
name: task-decomposition-checkpointing
description: Break requests into small checkpoints with verify steps and stop-on-fail behavior. Use when tasks span multiple files or systems.
---

# Task Decomposition and Checkpointing

## Goal
Reduce surprise regressions through gated incremental delivery.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Checkpoint list based on `../_shared/checkpoint-template.md`.

## Verify Gate
No checkpoint closes without a passing command or assertion result.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
