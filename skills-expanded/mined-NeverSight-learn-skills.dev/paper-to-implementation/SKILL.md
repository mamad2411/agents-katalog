---
name: paper-to-implementation
description: Use when translating a paper idea into code, deciding whether a paper is worth reproducing, or planning a faithful paper-based experiment
---

# Paper To Implementation

Separate what the paper actually contributes from what its codebase or benchmark setup happened to do.

## Workflow

1. Extract the paper's core intervention:
   - model change
   - loss change
   - data or augmentation change
   - training schedule change
   - evaluation change
2. Identify hidden assumptions:
   - dataset scale
   - pretraining
   - extra filtering
   - compute budget
   - ensemble or post-processing
3. Map the intervention into the current codebase.
4. Define the smallest faithful reproduction.
5. Define an ablation ladder:
   - reproduction
   - simplified local version
   - one-at-a-time ablations
6. Hand off to `experiment-design`.

## Guardrails

- Do not merge multiple paper ideas into one first attempt.
- Do not copy reported numbers without matching their protocol.
- If the paper's gains depend on infrastructure you do not have, state that early.
