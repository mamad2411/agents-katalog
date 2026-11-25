---
name: formax-test-stability-workflow
description: Use when adding or fixing Formax tests (especially Ink UI tests) and you need deterministic synchronization in test interactions.
---

# Formax Test Stability Workflow

## Goal
- Write stable UI tests with explicit state sync.

## Do
- Wait for target state before next key (example: wait `❯ 3.` before typing feedback).
- Assert final behavior, not transient cursor frames (example: assert feedback `aXb`, not `a▏b`).
- In multi-step input flows, wait for idle state between steps (example: placeholder/queue-hint settled).

- Extract repeated sync steps into local helpers (example: `selectFeedbackRow`, `queueMessageWhileLoading`).

## Don't
- Do not fix flakes by only increasing timeout.
- Do not use long sleep as synchronization.
- Do not bind assertions to fragile render glyphs/spacing.
