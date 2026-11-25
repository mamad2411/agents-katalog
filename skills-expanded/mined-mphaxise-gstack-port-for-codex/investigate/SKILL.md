---
name: investigate
description: Root-cause-first debugging for Codex. Use when the user reports a bug, unexpected behavior, or an error and wants investigation before speculative fixes.
---

# Investigate

Use this skill when the user is debugging and the right move is to understand the failure before making code changes.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Core Rule

No blind fixes without a root-cause theory.

## Workflow

1. Reproduce or inspect the failure surface:
   - error text
   - logs
   - changed files
   - runtime conditions
2. Gather evidence before editing code.
3. State the most likely hypotheses and what would confirm or falsify them.
4. Identify the most plausible root cause.
5. Only then implement the smallest fix that addresses that cause.
6. Re-run the relevant verification and confirm the symptom is gone for the right reason.

## Guardrails

- Do not stack multiple speculative fixes into one attempt.
- Do not edit code before you can name a concrete root-cause theory, unless the user explicitly asks for a quick experiment.
- If the bug cannot be reproduced, report the missing evidence and the next best diagnostic step.
- Prefer timeline and data-flow reasoning over guesswork.

## Outputs

Always include:

- observed symptom
- evidence gathered
- hypotheses considered
- most likely root cause
- fix plan or fix applied
- verification result
- remaining uncertainty, if any
